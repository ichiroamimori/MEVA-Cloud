# Robot retarget assets

Production IK uses the Robot Variant's approved MEVA Offset asset. It does not
generate or select an Offset from `workspace/`.

Each enabled Variant must declare one of these policies in `manifest.json`:

```json
"retarget_assets": {
  "meva_offsets": {
    "policy": "approved",
    "file": "retarget_assets/meva/approved_offsets.json",
    "sha256": "<raw-file-sha256>"
  }
}
```

Use `{"policy": "none"}` only when the Robot's mapping frames intentionally
require identity offsets.

For Robot installation or setup, generate a workspace candidate explicitly:

```text
python -m server.retarget.check_offsets path/to/config.json --force
```

Review the candidate with the Robot Viewer and regression motions. After the
manifest declares its destination, `--approve` copies the reviewed candidate
to that path and prints the new SHA256. Update the manifest SHA256 and include
both files in source control. A changed MJCF, canonical geometry, Robot
retargeting metadata, algorithm, or mapping identity invalidates the approved
asset until a new candidate is reviewed.

The approved asset may contain a superset of mappings. Each production Config
mapping must match an approved `(source_segment, target_link,
orientation_mode)` entry. Mapping weights and other solver settings remain Job
Config data and do not alter the geometric Offset.
