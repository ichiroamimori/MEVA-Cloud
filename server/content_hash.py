from __future__ import annotations

import hashlib
from pathlib import Path


CANONICAL_TEXT_SHA256 = "canonical-text-sha256-v1"
CANONICAL_JSON_SHA256 = "canonical-json-sha256-v1"
MUJOCO_ASSET_BUNDLE_SHA256 = "mujoco-asset-bundle-sha256-v2"

TEXT_ASSET_SUFFIXES = {
    ".csv", ".json", ".mjcf", ".mtl", ".obj", ".toml", ".txt",
    ".urdf", ".xml", ".yaml", ".yml",
}


def sha256_file(path: Path) -> str:
    """Hash exact bytes for transfer integrity and binary assets."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_text_bytes(value: bytes) -> bytes:
    """Normalize platform line endings without changing other text bytes."""
    return value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_text_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_text_bytes(path.read_bytes())).hexdigest()


def repository_asset_sha256(path: Path) -> str:
    """Hash Git-managed text canonically and binary assets byte-for-byte."""
    if path.suffix.lower() in TEXT_ASSET_SUFFIXES:
        return canonical_text_sha256(path)
    return sha256_file(path)
