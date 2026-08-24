from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from server.api.retarget_api import router as retarget_router


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"

app = FastAPI(title="MEVA Cloud Local")

# Register API first; the static "/" mount must come last.
app.include_router(retarget_router)

app.mount(
    "/",
    StaticFiles(directory=str(APP_DIR), html=True),
    name="app",
)
