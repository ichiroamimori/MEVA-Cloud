# Remote IK worker

MEVA Cloud can keep its Web UI and artifact storage on one PC while Primary/Main
IK runs on a separate Windows PC. The worker launches the existing
`primary_retarget.py` and `main_retarget.py` processes with the same Python,
Mink, MuJoCo, robot registry, and robot assets as local execution.

## Remote PC

Use the same MEVA Cloud revision on the Remote PC. It must contain the installed
robot manifests, MJCF files, and meshes under `server/robots`.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r server\requirements-worker.txt
$env:MEVA_IK_WORKER_TOKEN = "replace-with-a-long-random-token"
$env:MEVA_IK_WORKER_HOST = "100.x.y.z"
$env:MEVA_IK_WORKER_PORT = "8010"
.\.venv\Scripts\python.exe -m server.remote_ik_worker
```

Bind `MEVA_IK_WORKER_HOST` to the Remote PC's Tailscale address and restrict the
Windows firewall rule to the Tailscale interface/network. Do not expose this
initial worker directly to the public Internet.

The worker exposes health, submit, status, cancel, and result endpoints only. It has one
FIFO execution thread, so one IK process runs at a time. Status and logs are kept
under `workspace/remote_ik_worker/jobs/<job_id>` on the Remote PC. There is no
endpoint for executing a supplied command or Python source.
The job endpoints return HTTP 503 until `MEVA_IK_WORKER_TOKEN` is configured;
only `/health` is unauthenticated.

## MEVA Cloud PC

Set these variables before starting the existing server:

```powershell
$env:MEVA_IK_BACKEND = "remote_python"
$env:MEVA_REMOTE_IK_URL = "http://100.x.y.z:8010"
$env:MEVA_REMOTE_IK_TOKEN = "replace-with-a-long-random-token"
```

Start MEVA Cloud normally. Existing Retarget buttons, polling, and result screens
remain the same. Leave `MEVA_IK_BACKEND` unset, or set it to `local_python`, to use
the original local subprocess route.

On the Retargeting page, open the `Local user` menu and choose `Your PC` or
`Compute PC`. That browser selection is saved locally and applies to the next
Primary or Main job. It overrides `MEVA_IK_BACKEND` for that job; browsers that
have not made a selection continue to use the server environment default.

Optional settings are `MEVA_REMOTE_IK_POLL_SEC` (default 2),
`MEVA_REMOTE_IK_HTTP_TIMEOUT_SEC` (per network operation, default 60), and the
worker-side `MEVA_IK_MAX_ARCHIVE_BYTES` / `MEVA_IK_MAX_UNCOMPRESSED_BYTES`.
`MEVA_IK_JOB_TIMEOUT_SEC` limits each Local or Remote Python solver process
(default 7200 seconds). `MEVA_IK_JOB_TTL_SEC` controls how long a Worker keeps
terminal status/result files, and `MEVA_CLOUD_IK_JOB_TTL_SEC` controls Cloud job
status retention (both default to seven days).
Result downloads are capped by `MEVA_IK_MAX_RESULT_ARCHIVE_BYTES` (default 2
GiB) and extracted content by `MEVA_IK_MAX_RESULT_UNCOMPRESSED_BYTES` (default 4
GiB).

## Transfer contract

`POST /api/v1/ik/jobs` accepts an `application/zip` package containing versioned
`request.json` and checksum-declared files. MEVA data and Primary inputs remain
binary files rather than large JSON values. The manifest identifies a robot by
manufacturer/model/variant; it never sends the Cloud PC's absolute path. The
worker resolves the MJCF and meshes from its own registry.
The request carries both the legacy raw-byte `manifest_sha256` and
`manifest_json_sha256`, whose algorithm is identified as
`canonical-json-sha256-v1`. The latter parses the JSON, serializes it as sorted,
compact UTF-8 JSON, and hashes those bytes. Therefore checkout line endings,
trailing newlines, indentation, and object key order do not cause a mismatch.
Values and keys still affect the hash. A new worker prefers the canonical hash
and falls back to the legacy raw hash for an older request. MJCF and referenced
mesh/texture assets continue to use raw-byte SHA-256 and are not canonicalized.
The worker rejects a model revision mismatch before starting IK.

`GET /api/v1/ik/jobs/{job_id}` returns `queued`, `running`, `cancelling`,
`cancelled`, `completed`, or `failed`, plus frame progress and a stable error
code. `POST /api/v1/ik/jobs/{job_id}/cancel` cancels only a job owned by this
Worker; it cannot accept a PID or command. Result artifacts are
downloaded from `GET /api/v1/ik/jobs/{job_id}/result` as ZIP. Current workers
write `meva_ik_result_zip_v2`: `result.json` binds the archive to the stage,
Cloud job ID, artifact ID, status, exact allowed file set, byte sizes, and
SHA-256 hashes. Cloud rejects older manifest-less result ZIPs, so update the
Cloud server and Remote Worker to the same revision. Remote Main PKL data is
verified but never unpickled; Cloud rebuilds the compatibility PKL from the
verified canonical Main NPZ.

Worker job state is restored from each `status.json` on startup. Queued requests
are requeued, while a job interrupted during execution is marked failed with
`worker_restarted` rather than being run twice. Request archives, extracted
packages, and execution directories are removed after execution; terminal
status, logs, and result archives remain until their TTL expires. Cloud keeps a
small status record under `workspace/runtime/retarget_jobs` so a browser can
still inspect a terminal job after a server restart. A Local or Remote job that
was being coordinated when Cloud itself stopped is marked `cloud_restarted`.

This version implements `remote_python`. A future Remote DLL replaces the worker's
execution function below this contract. A future localhost bridge can expose the
same contract for Local DLL execution.

The worker requirements pin Python-facing packages and the Mink Git revision
`e3316cd7d210d64443655da061e88e3f5863f035`. Keep Python 3.13, the source
revision, and robot assets equal on both PCs.
For a reproducibility check, compare frame counts and the `root_pos`, `root_rot`,
and `dof_pos` arrays in local and remote NPZ output. Exact archive bytes can differ
because ZIP and metadata timestamps are not numerical result data.

Two optional developer checks are included:

```powershell
.\.venv\Scripts\python.exe scripts\check_remote_ik_http.py <primary-config> --url http://100.x.y.z:8010 --token <token>
.\.venv\Scripts\python.exe scripts\check_remote_ik_repro.py <primary-config> --main-config <main-config> --frames 2
```
