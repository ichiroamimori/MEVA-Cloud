from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException

from server.api.capsule_api import (
    CapsulePlacementRequest,
    FolderCreateRequest,
    create_capsule_folder,
    delete_capsule_folder,
    list_capsule_library,
    place_capsule,
    rename_capsule_folder,
    FolderUpdateRequest,
    unshare_capsule,
)


class CapsuleLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary.name) / "workspace"
        self.environment = patch.dict(
            os.environ,
            {"MEVA_WORKSPACE_ROOT": str(self.workspace)},
        )
        self.environment.start()
        self.capsule_id = "2609130001"
        capsule = self.workspace / "users" / "local_user" / "capsules" / self.capsule_id
        capsule.mkdir(parents=True)
        (capsule / "metadata.json").write_text(
            json.dumps({"capsule_id": self.capsule_id, "title": "Walking"}),
            encoding="utf-8",
        )
        self.capsule_path = capsule

    def tearDown(self) -> None:
        self.environment.stop()
        self.temporary.cleanup()

    def test_existing_capsules_default_to_personal_root(self) -> None:
        personal = list_capsule_library(scope="personal", folder_id="root")
        shared = list_capsule_library(scope="workspace", folder_id="root")
        self.assertEqual([item["id"] for item in personal["capsules"]], [self.capsule_id])
        self.assertEqual(shared["capsules"], [])
        self.assertEqual(personal["breadcrumbs"][0]["display_name"], "My Data")

    def test_virtual_folder_moves_reference_without_moving_capsule(self) -> None:
        folder = create_capsule_folder(
            FolderCreateRequest(
                scope="personal",
                parent_folder_id="root",
                display_name="Walking",
            )
        )["folder"]
        place_capsule(
            self.capsule_id,
            CapsulePlacementRequest(scope="personal", folder_id=folder["folder_id"]),
        )
        self.assertEqual(list_capsule_library(scope="personal", folder_id="root")["capsules"], [])
        nested = list_capsule_library(scope="personal", folder_id=folder["folder_id"])
        self.assertEqual([item["id"] for item in nested["capsules"]], [self.capsule_id])
        self.assertTrue(self.capsule_path.is_dir())

        renamed = rename_capsule_folder(
            folder["folder_id"],
            FolderUpdateRequest(scope="personal", display_name="Walking Tests"),
        )
        self.assertEqual(renamed["folder"]["display_name"], "Walking Tests")
        with self.assertRaises(HTTPException) as context:
            delete_capsule_folder(folder["folder_id"], scope="personal")
        self.assertEqual(context.exception.status_code, 409)

        place_capsule(
            self.capsule_id,
            CapsulePlacementRequest(scope="personal", folder_id="root"),
        )
        deleted = delete_capsule_folder(folder["folder_id"], scope="personal")
        self.assertEqual(deleted["deleted"]["folder_id"], folder["folder_id"])

    def test_workspace_share_and_unshare_use_same_capsule(self) -> None:
        place_capsule(
            self.capsule_id,
            CapsulePlacementRequest(scope="workspace", folder_id="root"),
        )
        shared = list_capsule_library(scope="workspace", folder_id="root")
        self.assertEqual([item["id"] for item in shared["capsules"]], [self.capsule_id])
        self.assertTrue(self.capsule_path.is_dir())
        unshare_capsule(self.capsule_id)
        self.assertEqual(list_capsule_library(scope="workspace", folder_id="root")["capsules"], [])
        self.assertTrue(self.capsule_path.is_dir())

    def test_frontend_keeps_tiles_and_exposes_both_scopes(self) -> None:
        page = (Path(__file__).resolve().parents[1] / "app" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="myDataTab"', page)
        self.assertIn('id="sharedDataTab"', page)
        self.assertIn('className = "card folder-card"', page)
        self.assertIn("/api/capsules/library?", page)


if __name__ == "__main__":
    unittest.main()
