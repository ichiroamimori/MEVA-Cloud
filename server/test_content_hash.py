from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from server.content_hash import (
    canonical_text_sha256,
    repository_asset_sha256,
    sha256_file,
)
from server.ik_contract import CONTRACT_VERSION, IKRequest, mujoco_asset_fingerprint
from server.remote_ik_client import _robot_identity


class ContentHashTests(unittest.TestCase):
    def test_canonical_text_hash_ignores_platform_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            lf = root / "lf.xml"
            crlf = root / "crlf.xml"
            lf.write_bytes(b"<mujoco>\n  <worldbody/>\n</mujoco>\n")
            crlf.write_bytes(b"<mujoco>\r\n  <worldbody/>\r\n</mujoco>\r\n")

            self.assertNotEqual(sha256_file(lf), sha256_file(crlf))
            self.assertEqual(
                canonical_text_sha256(lf), canonical_text_sha256(crlf)
            )

    def test_mujoco_bundle_canonicalizes_xml_but_keeps_binary_raw(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            parent = Path(name)
            fingerprints = []
            for directory_name, newline in (("lf", b"\n"), ("crlf", b"\r\n")):
                root = parent / directory_name
                root.mkdir()
                model = root / "model.xml"
                model.write_bytes(newline.join((
                    b'<mujoco model="test">',
                    b'  <asset><mesh name="mesh" file="mesh.stl"/></asset>',
                    b'  <worldbody/>',
                    b'</mujoco>',
                    b'',
                )))
                (root / "mesh.stl").write_bytes(b"binary\r\nmesh\x00")
                fingerprints.append(mujoco_asset_fingerprint(model, root))

            self.assertEqual(fingerprints[0], fingerprints[1])
            binary = parent / "binary.stl"
            binary.write_bytes(b"a\r\nb")
            self.assertEqual(repository_asset_sha256(binary), sha256_file(binary))

    def test_registered_g1_and_k1_use_canonical_robot_identity_hashes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for manufacturer, robot_id, variant, expected_model_hash in (
            (
                "unitree", "g1", "g1_29dof",
                "dfcfd8b41d0980695d0e75d76fdfd9965f71431a1c67afc31c8dbe730eb66c72",
            ),
            (
                "booster", "k1", "k1_22dof",
                "51954b1317d1afd386da28a5b28ebe7a536d79b94ded8ab61358daa3ab50bf83",
            ),
        ):
            identity = _robot_identity({
                "robot": {
                    "manufacturer": manufacturer,
                    "model": robot_id,
                    "variant": variant,
                }
            }, root)
            self.assertEqual(
                identity["model_hash_algorithm"], "canonical-text-sha256-v1"
            )
            self.assertEqual(identity["model_sha256"], expected_model_hash)
            self.assertEqual(
                identity["asset_bundle_hash_algorithm"],
                "mujoco-asset-bundle-sha256-v2",
            )
            self.assertEqual(
                identity["offset_asset_hash_algorithm"],
                "canonical-json-sha256-v1",
            )
            request = IKRequest.from_dict({
                "schema_version": CONTRACT_VERSION,
                "backend": "remote_python",
                "stage": "primary",
                "client_job_id": "hash-test",
                "robot": identity,
                "config_path": "inputs/config.json",
                "files": [
                    {
                        "role": "config", "path": "inputs/config.json",
                        "size": 0, "sha256": "1" * 64,
                    },
                    {
                        "role": "source", "path": "inputs/source.bin",
                        "size": 0, "sha256": "2" * 64,
                    },
                ],
            })
            self.assertEqual(request.robot["model_sha256"], expected_model_hash)


if __name__ == "__main__":
    unittest.main()
