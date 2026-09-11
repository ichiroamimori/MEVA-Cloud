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
.\.venv\Scripts\python.exe -m pip install -r server\requirements.txt
$env:MEVA_IK_WORKER_TOKEN = "replace-with-a-long-random-token"
$env:MEVA_IK_WORKER_HOST = "100.x.y.z"
$env:MEVA_IK_WORKER_PORT = "8010"
.\.venv\Scripts\python.exe -m server.remote_ik_worker
```

Bind `MEVA_IK_WORKER_HOST` to the Remote PC's Tailscale address and restrict the
Windows firewall rule to the Tailscale interface/network. Do not expose this
initial worker directly to the public Internet.

The worker exposes health, submit, status, and result endpoints only. It has one
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

Optional settings are `MEVA_REMOTE_IK_POLL_SEC` (default 2),
`MEVA_REMOTE_IK_HTTP_TIMEOUT_SEC` (per network operation, default 60), and the
worker-side `MEVA_IK_MAX_ARCHIVE_BYTES` / `MEVA_IK_MAX_UNCOMPRESSED_BYTES`.

## Transfer contract

`POST /api/v1/ik/jobs` accepts an `application/zip` package containing versioned
`request.json` and checksum-declared files. MEVA data and Primary inputs remain
binary files rather than large JSON values. The manifest identifies a robot by
manufacturer/model/variant; it never sends the Cloud PC's absolute path. The
worker resolves the MJCF and meshes from its own registry.
The request also carries SHA-256 values for the selected manifest, MJCF, and all
mesh/texture assets referenced by that MJCF. The worker rejects a model revision
mismatch before starting IK.

`GET /api/v1/ik/jobs/{job_id}` returns `queued`, `running`, `completed`, or
`failed`, plus frame progress and a stable error code. Result artifacts are
downloaded from `GET /api/v1/ik/jobs/{job_id}/result` as ZIP.

This version implements `remote_python`. A future Remote DLL replaces the worker's
execution function below this contract. A future localhost bridge can expose the
same contract for Local DLL execution.

Keep Python/package versions, source revision, and robot assets equal on both PCs.
For a reproducibility check, compare frame counts and the `root_pos`, `root_rot`,
and `dof_pos` arrays in local and remote NPZ output. Exact archive bytes can differ
because ZIP and metadata timestamps are not numerical result data.

Two optional developer checks are included:

```powershell
.\.venv\Scripts\python.exe scripts\check_remote_ik_http.py <primary-config> --url http://100.x.y.z:8010 --token <token>
.\.venv\Scripts\python.exe scripts\check_remote_ik_repro.py <primary-config> --main-config <main-config> --frames 2
```
