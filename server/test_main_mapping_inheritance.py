from __future__ import annotations

import unittest

from server.retarget_config_store import overlay_main_mapping_parameters


class MainMappingInheritanceTests(unittest.TestCase):
    def test_main_config_cannot_remove_primary_foot_mappings(self) -> None:
        primary = {
            "mappings": [
                {
                    "source_segment": "Thoracic2",
                    "target_link": "Trunk",
                    "orientation_weight": 1.0,
                },
                {
                    "source_segment": "LeftFoot",
                    "target_link": "left_foot_link",
                    "orientation_weight": 1.0,
                },
                {
                    "source_segment": "RightFoot",
                    "target_link": "right_foot_link",
                    "orientation_weight": 1.0,
                },
            ]
        }
        main = {
            "mappings": [{
                "source_segment": "Thoracic2",
                "target_link": "Trunk",
                "orientation_weight": 0.4,
            }]
        }

        mappings = overlay_main_mapping_parameters(
            primary["mappings"], main["mappings"]
        )

        self.assertEqual(
            [mapping["source_segment"] for mapping in mappings],
            ["Thoracic2", "LeftFoot", "RightFoot"],
        )
        self.assertEqual(mappings[0]["orientation_weight"], 0.4)
        self.assertEqual(mappings[1]["orientation_weight"], 1.0)
        self.assertEqual(mappings[2]["orientation_weight"], 1.0)

    def test_main_config_can_tune_but_not_redirect_primary_mapping(self) -> None:
        primary = {
            "mappings": [{
                "source_segment": "LeftFoot",
                "target_link": "left_foot_link",
                "orientation_weight": 1.0,
                "orientation_mode": "full",
            }]
        }
        main = {
            "mappings": [{
                "source_segment": "LeftLowerLeg",
                "target_link": "left_foot_link",
                "orientation_weight": 0.25,
                "orientation_mode": "axis",
            }]
        }

        mappings = overlay_main_mapping_parameters(
            primary["mappings"], main["mappings"]
        )

        self.assertEqual(mappings[0]["source_segment"], "LeftFoot")
        self.assertEqual(mappings[0]["target_link"], "left_foot_link")
        self.assertEqual(mappings[0]["orientation_weight"], 0.25)
        self.assertEqual(mappings[0]["orientation_mode"], "axis")


if __name__ == "__main__":
    unittest.main()
