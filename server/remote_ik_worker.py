from __future__ import annotations

import hmac
import json
import logging
import os
import queue
import shutil
import threading
import time
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse

from server.ik_contract import (
    IKContractError,
    IKRequest,
    extract_request_archive,
    read_request_manifest,
)
from server.ik_execution import IKExecutionError, run_python_ik


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKER_ROOT = REPOSITORY_ROOT / "workspace" / "remote_ik_worker"
MAX_ARCHIVE_BYTES = int(os.environ.get("MEVA_IK_MAX_ARCHIVE_BYTES", str(2 * 1024**3)))
MAX_UNCOMPRESSED_BYTES = int(
    os.environ.get("MEVA_IK_MAX_UNCOMPRESSED_BYTES", str(4 * 1024**3))
)
LOGGER = logging.getLogger("meva.remote_ik")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _zip_output(source: Path, destination: Path) -> list[str]:
    files = sorted(path for path in source.rglob("*") if path.is_file())
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(source).as_posix())
    return [path.relative_to(source).as_posix() for path in files]


class RemoteIKService:
    """One-process, one-at-a-time queue for a dedicated IK worker PC."""

    def __init__(self, root: Path = WORKER_ROOT):
        self.root = root
        self.jobs_root = root / "jobs"
        self.jobs_root.mkdir(parents=True, exist_ok=True)
        self.jobs: dict[str, dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.pending: queue.Queue[str] = queue.Queue()
        self.thread = threading.Thread(target=self._worker_loop, daemon=True, name="remote-ik-worker")
        self.thread.start()

    def submit(self, archive_path: Path, request: IKRequest) -> dict[str, Any]:
        job_id = uuid.uuid4().hex
        job_dir = self.jobs_root / job_id
        job_dir.mkdir(parents=False, exist_ok=False)
        stored_archive = job_dir / "request.zip"
        try:
            archive_path.replace(stored_archive)
            package_dir = job_dir / "package"
            extract_request_archive(
                stored_archive, package_dir, request,
                max_uncompressed_bytes=MAX_UNCOMPRESSED_BYTES,
            )
        except Exception:
            shutil.rmtree(job_dir, ignore_errors=True)
            raise
        now = _utc_now()
        job = {
            "job_id": job_id,
            "client_job_id": request.client_job_id,
            "schema_version": request.schema_version,
            "backend": request.backend,
            "stage": request.stage,
            "robot": dict(request.robot),
            "status": "queued",
            "progress": 0.0,
            "processed": 0,
            "total": None,
            "source_frame": None,
            "message": "Queued",
            "submitted_at": now,
            "started_at": None,
            "finished_at": None,
            "elapsed_sec": None,
            "result_available": False,
            "files": [],
            "error": None,
        }
        with self.lock:
            self.jobs[job_id] = job
            self._persist(job_id)
        LOGGER.info(
            "job_id=%s status=queued client_job_id=%s stage=%s robot=%s/%s/%s",
            job_id, request.client_job_id, request.stage,
            request.robot["manufacturer"], request.robot["robot_id"], request.robot["variant"],
        )
        self.pending.put(job_id)
        return dict(job)

    def status(self, job_id: str) -> dict[str, Any] | None:
        with self.lock:
            job = self.jobs.get(job_id)
            return dict(job) if job is not None else None

    def result_path(self, job_id: str) -> Path | None:
        job = self.status(job_id)
        path = self.jobs_root / job_id / "result.zip"
        return path if job and job["result_available"] and path.is_file() else None

    def _persist(self, job_id: str) -> None:
        _write_json(self.jobs_root / job_id / "status.json", self.jobs[job_id])

    def _update(self, job_id: str, **values: Any) -> None:
        with self.lock:
            self.jobs[job_id].update(values)
            self._persist(job_id)

    def _worker_loop(self) -> None:
        while True:
            job_id = self.pending.get()
            try:
                self._run(job_id)
            except Exception as exc:
                LOGGER.exception("job_id=%s unexpected worker-loop failure", job_id)
                try:
                    self._update(
                        job_id,
                        status="failed",
                        message="IK failed",
                        finished_at=_utc_now(),
                        error={
                            "code": "unexpected_exception",
                            "message": f"{type(exc).__name__}: {exc}",
                        },
                    )
                except Exception:
                    LOGGER.exception("job_id=%s could not persist worker-loop failure", job_id)
            finally:
                self.pending.task_done()

    def _run(self, job_id: str) -> None:
        job_dir = self.jobs_root / job_id
        request = read_request_manifest(job_dir / "request.zip")
        started = time.monotonic()
        self._update(
            job_id, status="running", message="Preparing...", started_at=_utc_now(),
        )
        LOGGER.info("job_id=%s status=running", job_id)

        def progress(done: int, total: int, source_frame: int) -> None:
            self._update(
                job_id,
                processed=done,
                total=total,
                source_frame=source_frame,
                progress=(done / total) if total else 0.0,
                message=f"{done} / {total} frames",
            )

        output_directory: Path | None = None
        logs: list[str] = []
        status = "completed"
        error: dict[str, str] | None = None
        try:
            result = run_python_ik(
                request,
                job_dir / "package",
                job_dir / "execution",
                REPOSITORY_ROOT,
                progress,
            )
            output_directory = result.output_directory
            logs = list(result.logs)
        except IKExecutionError as exc:
            status = "failed"
            error = {"code": exc.code, "message": str(exc)}
            logs = exc.logs
            output_directory = exc.output_directory
        except Exception as exc:
            status = "failed"
            error = {"code": "unexpected_exception", "message": f"{type(exc).__name__}: {exc}"}
            LOGGER.exception("job_id=%s unexpected execution error", job_id)

        (job_dir / "worker.log").write_text("\n".join(logs) + ("\n" if logs else ""), encoding="utf-8")
        files: list[str] = []
        result_available = False
        if output_directory is not None and output_directory.is_dir():
            try:
                files = _zip_output(output_directory, job_dir / "result.zip")
                result_available = True
            except Exception as exc:
                status = "failed"
                error = {"code": "output_write_failure", "message": str(exc)}
        elapsed = time.monotonic() - started
        self._update(
            job_id,
            status=status,
            progress=1.0 if status == "completed" else self.status(job_id)["progress"],
            message="Completed" if status == "completed" else "IK failed",
            finished_at=_utc_now(),
            elapsed_sec=elapsed,
            result_available=result_available,
            files=files,
            error=error,
        )
        LOGGER.info(
            "job_id=%s status=%s elapsed_sec=%.3f files=%d error=%s",
            job_id, status, elapsed, len(files), error,
        )


service = RemoteIKService()
app = FastAPI(title="MEVA Remote IK Worker", version="1.0")


def _authorize(authorization: str | None) -> None:
    expected = os.environ.get("MEVA_IK_WORKER_TOKEN", "")
    if not expected:
        raise HTTPException(status_code=503, detail="MEVA_IK_WORKER_TOKEN is not configured")
    supplied = authorization or ""
    prefix = "Bearer "
    if not supplied.startswith(prefix) or not hmac.compare_digest(supplied[len(prefix):], expected):
        raise HTTPException(status_code=401, detail="Invalid worker token")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "backend": "remote_python", "contract_version": "1.0"}


@app.post("/api/v1/ik/jobs", status_code=202)
async def submit_job(request: Request, authorization: str | None = Header(default=None)):
    _authorize(authorization)
    if request.headers.get("content-type", "").split(";", 1)[0].strip() != "application/zip":
        raise HTTPException(status_code=415, detail="Content-Type must be application/zip")
    upload = service.root / f".upload-{uuid.uuid4().hex}.zip"
    size = 0
    try:
        with upload.open("wb") as output:
            async for chunk in request.stream():
                size += len(chunk)
                if size > MAX_ARCHIVE_BYTES:
                    raise HTTPException(status_code=413, detail="IK request archive is too large")
                output.write(chunk)
        contract = read_request_manifest(upload)
        if contract.backend != "remote_python":
            raise IKContractError("This worker only implements remote_python")
        return service.submit(upload, contract)
    except IKContractError as exc:
        raise HTTPException(status_code=400, detail={"code": "invalid_request", "message": str(exc)}) from exc
    finally:
        upload.unlink(missing_ok=True)


@app.get("/api/v1/ik/jobs/{job_id}")
def get_job(job_id: str, authorization: str | None = Header(default=None)):
    _authorize(authorization)
    job = service.status(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/api/v1/ik/jobs/{job_id}/result")
def get_result(job_id: str, authorization: str | None = Header(default=None)):
    _authorize(authorization)
    job = service.status(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    path = service.result_path(job_id)
    if path is None:
        raise HTTPException(status_code=409, detail="Result is not available")
    return FileResponse(path, media_type="application/zip", filename=f"{job_id}.zip")


def main() -> None:
    import uvicorn

    host = os.environ.get("MEVA_IK_WORKER_HOST", "127.0.0.1")
    port = int(os.environ.get("MEVA_IK_WORKER_PORT", "8010"))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    uvicorn.run("server.remote_ik_worker:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
