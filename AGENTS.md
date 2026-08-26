# MEVA Cloud — Agent Instructions

## General

This repository contains the MEVA Cloud application.

Make only the changes necessary for the requested task.
Preserve the existing architecture, behavior, and file structure unless a change is explicitly required.

Prefer small, localized changes over broad rewrites or refactoring.

## Git Safety

The Git repository and its history are managed by the user.

### Allowed

Read-only Git commands may be used when useful for understanding or verifying changes, including:

- `git status`
- `git diff`
- `git log`
- `git show`
- `git branch` when used only for inspection

### Prohibited unless explicitly requested by the user

Do not perform any operation that changes Git state, history, branches, remotes, or the working tree through Git.

This includes, but is not limited to:

- `git init`
- `git add`
- `git commit`
- `git push`
- `git pull`
- `git fetch` when it would alter repository state
- `git merge`
- `git rebase`
- `git reset`
- `git restore`
- `git clean`
- `git checkout`
- `git switch`
- creating, deleting, or renaming branches or tags
- modifying remotes

Never modify, delete, move, replace, or recreate the `.git` directory or anything inside it.

Never delete and recreate the repository root as a way of modifying the project.

If a task appears to require a Git-changing operation, stop and ask the user first.

## File and Directory Safety

Do not perform broad or recursive deletion of files or directories unless explicitly requested.

In particular, do not use operations equivalent to:

- `rm -rf` on the project or a broad directory
- `rmdir /s`
- `Remove-Item -Recurse` on broad paths
- replacing the repository by copying a newly generated directory over it

When removing obsolete files is necessary, remove only specifically identified files.

Do not delete files merely because they appear unused without first confirming their role in the existing application.

## Workspace Data

`workspace/` contains runtime/user-generated MEVA Cloud data and is not source code.

Do not delete, reset, reorganize, overwrite, or bulk-modify anything under `workspace/` unless the user's task explicitly requires changes there.

Changes to application code must not depend on deleting existing workspace data.

## Existing User Data

Preserve existing uploaded capsules, generated data, configuration files, and user-created content.

When changing schemas or data formats, maintain backward compatibility where practical.

If a change could make existing user data unreadable or require migration, explain the impact before implementing it.

## Implementation

Before making a substantial change:

1. Inspect the relevant existing implementation.
2. Reuse existing patterns and utilities where practical.
3. Identify the smallest set of files that needs modification.

Do not create duplicate implementations when an existing module can reasonably be extended.

Avoid unrelated cleanup, formatting changes, renaming, or refactoring during a focused task.

## Verification

After changes:

1. Review the resulting diff.
2. Check for obvious syntax or import errors.
3. Run relevant tests or lightweight verification when available.
4. Report what was changed and any remaining limitations.

Do not alter files solely to make tests pass if doing so would change intended application behavior.

## Destructive or High-Risk Operations

Before any action that could cause significant data loss or make recovery difficult, stop and ask the user for explicit approval.

Examples include:

- deleting a directory containing multiple project files
- overwriting existing user data
- database or data-format migrations
- mass file moves or renames
- replacing generated or uploaded datasets
- changing repository or Git configuration

When uncertain whether an operation is destructive, treat it as destructive and ask first.