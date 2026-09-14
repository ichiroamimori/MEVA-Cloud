from __future__ import annotations

import csv
import json
import os
import re
import shutil
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from server.capsule_identity import CAPSULE_ID_RE, is_public_capsule
from server.service_context import (
    DEVELOPMENT_STORAGE_USER_ID,
    DEVELOPMENT_USER,
    DEVELOPMENT_WORKSPACE,
)


router = APIRouter(prefix="/api/capsules", tags=["capsules"])

UPLOAD_ID_RE = re.compile(r"^[0-9a-f]{32}$")
INVALID_FILENAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED_FILENAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
UPLOAD_LOCK = threading.Lock()


class UploadFileSpec(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    size: int = Field(ge=0)
    content_type: str = Field(default="application/octet-stream", max_length=255)


class UploadStartRequest(BaseModel):
    files: list[UploadFileSpec] = Field(min_length=1, max_length=1000)
    title: str = Field(min_length=1, max_length=200)
    note: str = Field(default="", max_length=2000)


class CapsuleUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    note: str = Field(default="", max_length=2000)


class FolderCreateRequest(BaseModel):
    scope: Literal["personal", "workspace"]
    parent_folder_id: str = Field(default="root", min_length=1, max_length=40)
    display_name: str = Field(min_length=1, max_length=100)


class FolderUpdateRequest(BaseModel):
    scope: Literal["personal", "workspace"]
    display_name: str = Field(min_length=1, max_length=100)


class CapsulePlacementRequest(BaseModel):
    scope: Literal["personal", "workspace"]
    folder_id: str = Field(default="root", min_length=1, max_length=40)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_root() -> Path:
    override = os.environ.get("MEVA_WORKSPACE_ROOT")
    return Path(override).resolve() if override else repo_root() / "workspace"


def capsules_root() -> Path:
    return workspace_root() / "users" / DEVELOPMENT_STORAGE_USER_ID / "capsules"


def uploads_root() -> Path:
    return workspace_root() / "users" / DEVELOPMENT_STORAGE_USER_ID / ".uploads"


def library_path() -> Path:
    return workspace_root() / "capsule_library.json"


def empty_library() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "folders": [],
        "personal_locations": {},
        "workspace_locations": {},
    }


def read_library() -> dict[str, Any]:
    try:
        value = json.loads(library_path().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return empty_library()
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=409, detail="Capsule library metadata is invalid") from exc
    if not isinstance(value, dict):
        raise HTTPException(status_code=409, detail="Capsule library metadata is invalid")
    result = empty_library()
    result.update(value)
    for key in ("folders", "personal_locations", "workspace_locations"):
        expected_type = list if key == "folders" else dict
        if not isinstance(result[key], expected_type):
            raise HTTPException(status_code=409, detail="Capsule library metadata is invalid")
    return result


def write_library(value: dict[str, Any]) -> None:
    path = library_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, value)


def folder_for_scope(library: dict[str, Any], scope: str, folder_id: str) -> dict[str, Any] | None:
    if folder_id == "root":
        return None
    folder = next(
        (item for item in library["folders"] if item.get("folder_id") == folder_id),
        None,
    )
    if not folder or folder.get("scope") != scope:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


def folder_breadcrumbs(library: dict[str, Any], scope: str, folder_id: str) -> list[dict[str, str]]:
    labels = {"personal": "My Data", "workspace": "Shared Data"}
    result = [{"folder_id": "root", "display_name": labels[scope]}]
    if folder_id == "root":
        return result
    by_id = {
        item.get("folder_id"): item
        for item in library["folders"]
        if item.get("scope") == scope
    }
    chain = []
    current_id = folder_id
    visited = set()
    while current_id != "root":
        if current_id in visited or current_id not in by_id:
            raise HTTPException(status_code=409, detail="Folder hierarchy is invalid")
        visited.add(current_id)
        current = by_id[current_id]
        chain.append({"folder_id": current_id, "display_name": str(current.get("display_name", ""))})
        current_id = str(current.get("parent_folder_id", "root"))
    result.extend(reversed(chain))
    return result


def folder_options(library: dict[str, Any], scope: str) -> list[dict[str, str]]:
    options = []
    for folder in library["folders"]:
        if folder.get("scope") != scope:
            continue
        folder_id = str(folder.get("folder_id", ""))
        crumbs = folder_breadcrumbs(library, scope, folder_id)
        options.append(
            {
                "folder_id": folder_id,
                "display_name": " / ".join(item["display_name"] for item in crumbs[1:]),
            }
        )
    options.sort(key=lambda item: item["display_name"].casefold())
    return [{"folder_id": "root", "display_name": "Root"}, *options]


def capsule_dir(capsule_id: str) -> Path:
    if not CAPSULE_ID_RE.fullmatch(capsule_id):
        raise HTTPException(status_code=404, detail="Capsule not found")
    root = capsules_root().resolve()
    path = (root / capsule_id).resolve()
    if path.parent != root or not path.is_dir():
        raise HTTPException(status_code=404, detail="Capsule not found")
    return path


def validate_filename(filename: str) -> str:
    if (
        filename in {".", ".."}
        or filename != filename.strip()
        or filename.endswith((".", " "))
        or INVALID_FILENAME_RE.search(filename)
        or Path(filename).name != filename
        or filename.split(".", 1)[0].upper() in RESERVED_FILENAMES
    ):
        raise HTTPException(status_code=400, detail=f"Invalid filename: {filename}")
    return filename


def upload_dir(upload_id: str) -> Path:
    if not UPLOAD_ID_RE.fullmatch(upload_id):
        raise HTTPException(status_code=404, detail="Upload session not found")
    return uploads_root() / upload_id


def read_manifest(upload_id: str) -> tuple[Path, dict[str, Any]]:
    session_dir = upload_dir(upload_id)
    manifest_path = session_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=404, detail="Upload session not found") from exc
    return session_dir, manifest


def write_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def cleanup_upload_session(session_dir: Path, manifest: dict[str, Any]) -> None:
    for index in range(len(manifest.get("files", []))):
        (session_dir / "files" / f"{index}.part").unlink(missing_ok=True)

    staging_capsule = session_dir / "capsule"
    for spec in manifest.get("files", []):
        filename = spec.get("name", "")
        if filename:
            (staging_capsule / "meva" / filename).unlink(missing_ok=True)
    (staging_capsule / "metadata.json").unlink(missing_ok=True)

    for directory in (
        staging_capsule / "meva",
        staging_capsule,
        session_dir / "files",
    ):
        try:
            directory.rmdir()
        except FileNotFoundError:
            pass
    (session_dir / "manifest.json").unlink(missing_ok=True)
    try:
        session_dir.rmdir()
    except FileNotFoundError:
        pass


def next_capsule_id(now: datetime) -> str:
    root = capsules_root()
    root.mkdir(parents=True, exist_ok=True)
    prefix = now.strftime("%y%m%d")
    if prefix == "000000":
        raise HTTPException(status_code=409, detail="Public Capsule prefix is reserved")
    existing = {
        path.name
        for path in root.iterdir()
        if path.is_dir() and CAPSULE_ID_RE.fullmatch(path.name)
    }
    for sequence in range(1, 10000):
        candidate = f"{prefix}{sequence:04d}"
        if candidate not in existing:
            return candidate
    raise HTTPException(status_code=409, detail="No Capsule ID is available today")


def parse_recording_datetime(csv_path: Path) -> datetime | None:
    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as source:
            rows = []
            reader = csv.reader(source)
            for _ in range(20):
                try:
                    rows.append(next(reader))
                except StopIteration:
                    break
    except (OSError, UnicodeDecodeError, csv.Error):
        rows = []

    date_value = ""
    time_value = ""
    for index, row in enumerate(rows):
        if not row or row[0].strip().casefold() != "time info":
            continue
        headers = [value.strip().casefold() for value in row]
        if index + 1 >= len(rows):
            break
        values = rows[index + 1]
        if "date" in headers:
            date_index = headers.index("date")
            if date_index < len(values):
                date_value = values[date_index].strip()
        if "time" in headers:
            time_index = headers.index("time")
            if time_index < len(values):
                time_value = values[time_index].strip()
        break

    date_formats = ("%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%d%m%y")
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_value, date_format).date()
            parsed_time = datetime.strptime(time_value, "%H:%M:%S").time() if time_value else datetime.min.time()
            return datetime.combine(parsed_date, parsed_time).astimezone()
        except ValueError:
            continue

    for match in re.finditer(r"(?:^|_)(\d{6})(?=_|\.|$)", csv_path.name):
        try:
            parsed_date = datetime.strptime(match.group(1), "%d%m%y").date()
            return datetime.combine(parsed_date, datetime.min.time()).astimezone()
        except ValueError:
            continue
    return None


def capsule_summary(capsule_dir: Path) -> dict[str, Any]:
    metadata_path = capsule_dir / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        metadata = {}

    source = metadata.get("meva_source") or {}
    files = metadata.get("files") or []
    source_name = source.get("original_filename") or Path(source.get("file", "")).name
    if not source_name and files:
        source_name = files[0].get("name", "")

    formats = []
    for item in files:
        suffix = Path(item.get("name", "")).suffix.lstrip(".").upper()
        if suffix and suffix not in formats:
            formats.append(suffix)
    source_format = str(source.get("format", "")).upper()
    if source_format and source_format not in formats:
        formats.insert(0, source_format)

    return {
        "id": capsule_dir.name,
        "is_public": is_public_capsule(capsule_dir.name),
        "title": metadata.get("title") or capsule_dir.name,
        "note": metadata.get("note", ""),
        "created_at": metadata.get("created_at", ""),
        "description": f"MEVAソースデータ: {source_name}" if source_name else "MEVAソースデータ",
        "modalities": ["MEVA", *formats],
    }


@router.get("")
def list_capsules() -> dict[str, list[dict[str, Any]]]:
    root = capsules_root()
    if not root.exists():
        return {"capsules": []}
    items = [
        capsule_summary(path)
        for path in root.iterdir()
        if path.is_dir() and CAPSULE_ID_RE.fullmatch(path.name)
    ]
    items.sort(key=lambda item: item["id"], reverse=True)
    return {"capsules": items}


@router.get("/library")
def list_capsule_library(
    scope: Literal["personal", "workspace"] = "personal",
    folder_id: str = "root",
) -> dict[str, Any]:
    library = read_library()
    folder_for_scope(library, scope, folder_id)
    root = capsules_root()
    summaries = {
        path.name: capsule_summary(path)
        for path in root.iterdir()
        if root.exists() and path.is_dir() and CAPSULE_ID_RE.fullmatch(path.name)
    } if root.exists() else {}
    locations_key = f"{scope}_locations"
    locations = library[locations_key]
    if scope == "personal":
        capsule_ids = [
            capsule_id
            for capsule_id in summaries
            if locations.get(capsule_id, "root") == folder_id
        ]
    else:
        capsule_ids = [
            capsule_id
            for capsule_id, location in locations.items()
            if location == folder_id and capsule_id in summaries
        ]
    capsules = []
    for capsule_id in capsule_ids:
        summary = dict(summaries[capsule_id])
        summary["owner_user_id"] = DEVELOPMENT_USER.user_id
        summary["shared_to_workspace"] = capsule_id in library["workspace_locations"]
        capsules.append(summary)
    capsules.sort(key=lambda item: item["id"], reverse=True)
    folders = [
        {
            "folder_id": str(item["folder_id"]),
            "display_name": str(item["display_name"]),
        }
        for item in library["folders"]
        if item.get("scope") == scope and item.get("parent_folder_id", "root") == folder_id
    ]
    folders.sort(key=lambda item: item["display_name"].casefold())
    return {
        "scope": scope,
        "workspace": {
            "workspace_id": DEVELOPMENT_WORKSPACE.workspace_id,
            "display_name": DEVELOPMENT_WORKSPACE.display_name,
        },
        "current_folder_id": folder_id,
        "breadcrumbs": folder_breadcrumbs(library, scope, folder_id),
        "folder_options": folder_options(library, scope),
        "folders": folders,
        "capsules": capsules,
    }


@router.post("/folders", status_code=201)
def create_capsule_folder(payload: FolderCreateRequest) -> dict[str, Any]:
    display_name = payload.display_name.strip()
    if not display_name:
        raise HTTPException(status_code=400, detail="Folder name is required")
    with UPLOAD_LOCK:
        library = read_library()
        folder_for_scope(library, payload.scope, payload.parent_folder_id)
        duplicate = any(
            item.get("scope") == payload.scope
            and item.get("parent_folder_id", "root") == payload.parent_folder_id
            and str(item.get("display_name", "")).casefold() == display_name.casefold()
            for item in library["folders"]
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="A folder with this name already exists")
        folder = {
            "folder_id": f"fld_{uuid.uuid4().hex}",
            "scope": payload.scope,
            "parent_folder_id": payload.parent_folder_id,
            "display_name": display_name,
            "created_by": DEVELOPMENT_USER.user_id,
            "workspace_id": DEVELOPMENT_WORKSPACE.workspace_id if payload.scope == "workspace" else None,
            "created_at": datetime.now().astimezone().isoformat(),
        }
        library["folders"].append(folder)
        write_library(library)
    return {"folder": folder}


@router.patch("/folders/{folder_id}")
def rename_capsule_folder(folder_id: str, payload: FolderUpdateRequest) -> dict[str, Any]:
    display_name = payload.display_name.strip()
    if not display_name:
        raise HTTPException(status_code=400, detail="Folder name is required")
    with UPLOAD_LOCK:
        library = read_library()
        folder = folder_for_scope(library, payload.scope, folder_id)
        assert folder is not None
        duplicate = any(
            item.get("folder_id") != folder_id
            and item.get("scope") == payload.scope
            and item.get("parent_folder_id", "root") == folder.get("parent_folder_id", "root")
            and str(item.get("display_name", "")).casefold() == display_name.casefold()
            for item in library["folders"]
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="A folder with this name already exists")
        folder["display_name"] = display_name
        folder["updated_at"] = datetime.now().astimezone().isoformat()
        write_library(library)
    return {"folder": folder}


@router.delete("/folders/{folder_id}")
def delete_capsule_folder(
    folder_id: str,
    scope: Literal["personal", "workspace"],
) -> dict[str, Any]:
    with UPLOAD_LOCK:
        library = read_library()
        folder = folder_for_scope(library, scope, folder_id)
        assert folder is not None
        has_children = any(
            item.get("scope") == scope and item.get("parent_folder_id") == folder_id
            for item in library["folders"]
        )
        has_capsules = folder_id in library[f"{scope}_locations"].values()
        if has_children or has_capsules:
            raise HTTPException(status_code=409, detail="Only empty folders can be deleted")
        library["folders"].remove(folder)
        write_library(library)
    return {"deleted": {"folder_id": folder_id, "display_name": folder["display_name"]}}


@router.put("/{capsule_id}/placement")
def place_capsule(capsule_id: str, payload: CapsulePlacementRequest) -> dict[str, Any]:
    capsule_dir(capsule_id)
    with UPLOAD_LOCK:
        library = read_library()
        folder_for_scope(library, payload.scope, payload.folder_id)
        library[f"{payload.scope}_locations"][capsule_id] = payload.folder_id
        write_library(library)
    return {
        "capsule_id": capsule_id,
        "scope": payload.scope,
        "folder_id": payload.folder_id,
    }


@router.delete("/{capsule_id}/placement/workspace")
def unshare_capsule(capsule_id: str) -> dict[str, Any]:
    capsule_dir(capsule_id)
    with UPLOAD_LOCK:
        library = read_library()
        removed = library["workspace_locations"].pop(capsule_id, None) is not None
        if removed:
            write_library(library)
    return {"capsule_id": capsule_id, "shared": False}


@router.put("/{capsule_id}")
def update_capsule(capsule_id: str, payload: CapsuleUpdateRequest) -> dict[str, Any]:
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Capsule name is required")

    with UPLOAD_LOCK:
        path = capsule_dir(capsule_id)
        metadata_path = path / "metadata.json"
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            metadata = {"schema_version": "1.0", "capsule_id": capsule_id}
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=409, detail="Capsule metadata is invalid") from exc

        metadata["title"] = title
        metadata["note"] = payload.note.strip()
        metadata["updated_at"] = datetime.now().astimezone().isoformat()
        write_json(metadata_path, metadata)

    return {"capsule": capsule_summary(path)}


@router.delete("/{capsule_id}")
def delete_capsule(capsule_id: str) -> dict[str, Any]:
    with UPLOAD_LOCK:
        path = capsule_dir(capsule_id)
        deleted = capsule_summary(path)
        shutil.rmtree(path)
        library = read_library()
        changed = False
        for key in ("personal_locations", "workspace_locations"):
            if library[key].pop(capsule_id, None) is not None:
                changed = True
        if changed:
            write_library(library)
    return {"deleted": deleted}


@router.post("/uploads")
def start_upload(payload: UploadStartRequest) -> dict[str, Any]:
    names = [validate_filename(item.name) for item in payload.files]
    normalized = [name.casefold() for name in names]
    if len(normalized) != len(set(normalized)):
        raise HTTPException(status_code=400, detail="Duplicate filenames are not supported")
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Capsule name is required")

    upload_id = uuid.uuid4().hex
    session_dir = uploads_root() / upload_id
    files_dir = session_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=False)
    manifest = {
        "upload_id": upload_id,
        "title": title,
        "note": payload.note.strip(),
        "created_at": datetime.now().astimezone().isoformat(),
        "files": [item.model_dump() for item in payload.files],
        "uploaded": [],
    }
    write_json(session_dir / "manifest.json", manifest)
    return {"upload_id": upload_id, "file_count": len(payload.files)}


@router.put("/uploads/{upload_id}/files/{file_index}")
async def upload_file(upload_id: str, file_index: int, request: Request) -> dict[str, Any]:
    session_dir, manifest = read_manifest(upload_id)
    files = manifest.get("files", [])
    if file_index < 0 or file_index >= len(files):
        raise HTTPException(status_code=404, detail="Upload file not found")

    expected_size = int(files[file_index]["size"])
    destination = session_dir / "files" / f"{file_index}.part"
    received = 0
    try:
        with destination.open("wb") as output:
            async for chunk in request.stream():
                received += len(chunk)
                if received > expected_size:
                    raise HTTPException(status_code=413, detail="Uploaded file exceeds declared size")
                output.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise

    if received != expected_size:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=f"Uploaded size mismatch: expected {expected_size}, received {received}",
        )

    with UPLOAD_LOCK:
        _, latest = read_manifest(upload_id)
        uploaded = set(int(value) for value in latest.get("uploaded", []))
        uploaded.add(file_index)
        latest["uploaded"] = sorted(uploaded)
        write_json(session_dir / "manifest.json", latest)

    return {"file_index": file_index, "received": received}


@router.delete("/uploads/{upload_id}")
def cancel_upload(upload_id: str) -> dict[str, bool]:
    with UPLOAD_LOCK:
        session_dir, manifest = read_manifest(upload_id)
        cleanup_upload_session(session_dir, manifest)
    return {"deleted": True}


@router.post("/uploads/{upload_id}/complete")
def complete_upload(upload_id: str) -> dict[str, Any]:
    with UPLOAD_LOCK:
        session_dir, manifest = read_manifest(upload_id)
        specs = manifest.get("files", [])
        uploaded = set(int(value) for value in manifest.get("uploaded", []))
        expected = set(range(len(specs)))
        if uploaded != expected:
            raise HTTPException(status_code=409, detail="Not all files have finished uploading")

        for index, spec in enumerate(specs):
            path = session_dir / "files" / f"{index}.part"
            if not path.is_file() or path.stat().st_size != int(spec["size"]):
                raise HTTPException(status_code=409, detail=f"Upload file {index} is incomplete")

        now = datetime.now().astimezone()
        staging_capsule = session_dir / "capsule"
        meva_dir = staging_capsule / "meva"
        meva_dir.mkdir(parents=True, exist_ok=False)

        file_metadata = []
        for index, spec in enumerate(specs):
            filename = validate_filename(spec["name"])
            source = session_dir / "files" / f"{index}.part"
            destination = meva_dir / filename
            source.replace(destination)
            file_metadata.append(
                {
                    "name": filename,
                    "path": f"meva/{filename}",
                    "size": int(spec["size"]),
                    "content_type": spec.get("content_type") or "application/octet-stream",
                }
            )

        source_file = next(
            (item for item in file_metadata if Path(item["name"]).suffix.lower() == ".csv"),
            file_metadata[0],
        )
        recording_at = (
            parse_recording_datetime(meva_dir / source_file["name"])
            if Path(source_file["name"]).suffix.lower() == ".csv"
            else None
        ) or now
        capsule_id = next_capsule_id(recording_at)
        source_suffix = Path(source_file["name"]).suffix.lstrip(".").lower()
        title = manifest["title"]
        note = manifest.get("note", "")
        metadata = {
            "schema_version": "1.0",
            "capsule_id": capsule_id,
            "title": title,
            "note": note,
            "created_at": now.isoformat(),
            "recording": {
                "date": recording_at.date().isoformat(),
                "time": recording_at.time().replace(microsecond=0).isoformat(),
                "recorded_at": recording_at.isoformat(),
            },
            "meva_source": {
                "type": "meva",
                "format": source_suffix,
                "file": source_file["path"],
                "original_filename": source_file["name"],
            },
            "files": file_metadata,
        }
        write_json(staging_capsule / "metadata.json", metadata)

        final_dir = capsules_root() / capsule_id
        if final_dir.exists():
            raise HTTPException(status_code=409, detail="Capsule ID already exists")
        staging_capsule.replace(final_dir)

        (session_dir / "manifest.json").unlink(missing_ok=True)
        (session_dir / "files").rmdir()
        session_dir.rmdir()

    return {"capsule": capsule_summary(final_dir)}
