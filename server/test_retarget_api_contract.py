from __future__ import annotations

import unittest
from pathlib import Path

from fastapi import FastAPI

from server.api.retarget_api import router
from server.api.retarget_config_api import _blank_primary_config
from server.api.retarget_robot_api import _runtime_robot_config
from server.robot_registry import resolve_variant, validate_retarget_config


EXPECTED_ROUTES = {
    ("GET", "/api/retarget/robots"),
    ("GET", "/api/retarget/configs"),
    ("GET", "/api/retarget/configs/load"),
    ("POST", "/api/retarget/configs"),
    ("GET", "/api/retarget/context"),
    ("GET", "/api/retarget/data-management"),
    ("POST", "/api/retarget/data-management/delete"),
    ("GET", "/api/retarget/viewer/validation"),
    ("GET", "/api/retarget/viewer/file/validation"),
    ("GET", "/api/retarget/main-targets/file"),
    ("GET", "/api/retarget/main-config"),
    ("POST", "/api/retarget/main/default"),
    ("GET", "/api/retarget/run-config"),
    ("POST", "/api/retarget/default"),
    ("POST", "/api/retarget/run-start"),
    ("POST", "/api/retarget/main/run-start"),
    ("GET", "/api/retarget/main/file"),
    ("GET", "/api/retarget/job/{job_id}"),
    ("POST", "/api/retarget/viewer/prepare"),
    ("GET", "/api/retarget/viewer/file/main-input"),
    ("GET", "/api/retarget/viewer/file/primary-post"),
    ("GET", "/api/retarget/viewer/file/retarget"),
    ("GET", "/api/retarget/viewer/file/meva"),
    ("POST", "/api/retarget/run"),
}


class RetargetApiContractTests(unittest.TestCase):
    def test_public_route_methods_and_paths_are_stable(self) -> None:
        app = FastAPI()
        app.include_router(router)

        def effective_routes(routes):
            for route in routes:
                candidates = getattr(route, "effective_candidates", None)
                if candidates is not None:
                    yield from effective_routes(candidates())
                else:
                    yield route

        actual = {
            (method, route.path)
            for route in effective_routes(app.routes)
            for method in (getattr(route, "methods", None) or set())
            if method not in {"HEAD", "OPTIONS"}
            and route.path.startswith("/api/retarget")
        }
        self.assertEqual(actual, EXPECTED_ROUTES)

    def test_variant_without_standard_config_gets_robot_neutral_blank_config(self) -> None:
        root = Path(__file__).resolve().parents[1]
        variant = resolve_variant("k1_22dof", root=root)
        config = _runtime_robot_config(_blank_primary_config(variant), variant)
        self.assertEqual(config["robot"]["manufacturer"], "booster")
        self.assertEqual(config["robot"]["variant"], "k1_22dof")
        self.assertEqual(config["mappings"], [])
        self.assertEqual(config["interframe_joint_acceleration_limit"]["overrides"], {})
        validate_retarget_config(variant, config)


if __name__ == "__main__":
    unittest.main()
