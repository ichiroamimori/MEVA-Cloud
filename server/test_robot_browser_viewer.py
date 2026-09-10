from __future__ import annotations

import unittest
from pathlib import Path

from fastapi import HTTPException

from server.api.retarget_robot_api import (
    get_browser_robot_viewer_asset,
    get_browser_robot_viewer_config,
)
from server.robot_browser_viewer import (
    RobotBrowserViewerError,
    browser_viewer_asset_paths,
    browser_viewer_config,
    resolve_browser_asset,
)
from server.robot_registry import resolve_variant


class RobotBrowserViewerTest(unittest.TestCase):
    def test_registered_mjcf_transitive_assets_are_browser_urls(self):
        for variant in ("g1_29dof", "k1_22dof"):
            with self.subTest(variant=variant):
                record = resolve_variant(variant)
                config = browser_viewer_config(record)
                paths = {item["path"] for item in config["files"]}
                self.assertIn(config["model_path"], paths)
                self.assertTrue(any(path.lower().endswith(".stl") for path in paths))
                self.assertTrue(all(not Path(path).is_absolute() for path in paths))
                self.assertTrue(all(".." not in Path(path).parts for path in paths))
                self.assertTrue(all(item["url"].startswith(
                    "/api/retarget/robots/viewer/browser/asset?"
                ) for item in config["files"]))
                self.assertEqual(config["initial_pose"], {"type": "model_default"})
                self.assertIsNone(config["standing_pose"])

    def test_asset_endpoint_only_serves_selected_mjcf_dependencies(self):
        record = resolve_variant("g1_29dof")
        paths = browser_viewer_asset_paths(record)
        model = record.model_path.relative_to(record.robot_directory).as_posix()
        self.assertEqual(resolve_browser_asset(record, model), record.model_path)
        with self.assertRaises(RobotBrowserViewerError):
            resolve_browser_asset(record, "../robots.json")
        with self.assertRaises(RobotBrowserViewerError):
            resolve_browser_asset(record, "g1_23dof.xml")

    def test_browser_config_api_keeps_selected_variant_and_motion_context(self):
        config = get_browser_robot_viewer_config(
            robot_variant="g1_29dof",
            manufacturer="unitree",
            robot_id="g1",
            capsule_id="2607010001",
            run_id="2609030003",
            stage="primary",
            main_id="legacy",
        )
        self.assertEqual(config["robot"]["robot_variant"], "g1_29dof")
        self.assertIn("run_id=2609030003", config["motion_url"])
        with self.assertRaises(HTTPException) as context:
            get_browser_robot_viewer_asset(
                path="../manifest.json",
                robot_variant="g1_29dof",
                manufacturer="unitree",
                robot_id="g1",
            )
        self.assertEqual(context.exception.status_code, 404)

    def test_web_ui_launcher_opens_independent_page_without_native_api(self):
        source = Path("app/assets/js/robot-viewer.js").read_text(encoding="utf-8")
        self.assertIn('window.open(`/robot-viewer/?${query}`', source)
        self.assertNotIn("/viewer/launch", source)
        self.assertTrue(Path("app/assets/robot-viewer/mujoco.wasm").is_file())
        self.assertTrue(Path("app/robot-viewer/index.html").is_file())


if __name__ == "__main__":
    unittest.main()
