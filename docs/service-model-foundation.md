# Service model foundation

This document records the compatibility boundary introduced before authentication,
billing, and role-based authorization are implemented.

## Development context

- User: `Xenoma_Admin_01` (`Zenosuke Miyamoto`, role `system_admin`)
- Workspace: `meva_development` (`MEVA Cloud Development`, plan `null`)
- Existing runtime data remains at `workspace/users/local_user`. `local_user` is a
  storage compatibility alias and is not the logical login ID.

Roles are `admin`, `user`, `worker`, `supervisor`, and `system_admin`. Plans are
`free`, `trial`, `standard`, and `enterprise`. They are data attributes only in
this phase; they do not authorize or limit any operation.

## Retargeting Config and Job

A reusable Retargeting Config records how to retarget. Its metadata is:

- `config_id`, `display_name`, `scope`, `owner_id`, `target_robot`
- `version`, `created_by`, `source_config_id`
- `created_at`, `updated_at`, `status`

Canonical scopes are `xenoma_standard`, `personal`, and `workspace`. Existing
`xenoma` and `user` values remain accepted as read aliases. Existing Config JSON
without metadata is normalized in memory and remains readable.

Capsule identity and the selected inclusive frame range belong to the Run snapshot
under `retarget_job`; they are removed when a reusable Config is saved. Publishing
a Personal Config creates a new Workspace `config_id` and records the Personal ID
in `source_config_id`. Archiving a Workspace Config sets `status` to `archived`;
the file remains available through APIs that explicitly include archived records.

Personal Configs use the same non-destructive Archive behavior and disappear from
the normal active selector. Replacing a Xenoma Standard is limited to Supervisor
and System Admin roles. Replacement creates a new `config_id`, links it to the old
generation through `source_config_id`, and retains the old generation as archived.
`standard_key` identifies the stable Robot/Stage Standard slot across generations.
Existing Run snapshots continue to retain the settings used at execution time.

## Capsule and MEVA BIN

Capsule IDs remain ten decimal digits. IDs beginning with `000000` are reserved
for Public Capsules; all other valid IDs are Private.

The current MEVA container is `MEVAVW02`, format version 6. It includes:

- `capsule_id` in the JSON header
- source frame, segment position/quaternion, joint position, and GCP blocks
- the paired BVH as an auxiliary `uint8` block for offset calculation

Readers still accept `MEVAVW01` and older `MEVAVW02` files for display and
inspection. Primary Compute requires the current format, so an older cached
MEVA BIN is regenerated from the authoritative Capsule source before a new Run.
Local and Remote Primary both consume this same BIN. Remote packaging rejects a
raw CSV source, and the Worker reads the authoritative Capsule ID and paired BVH
from the BIN.
