# Contributing to GodoGen

GodoGen exists to help coding agents produce better games autonomously while keeping results testable, recoverable and visibly proven.

## Repository model

The repository has two distinct layers:

- `skills/godogen` is the canonical source for the native Codex skill.
- User and project installations are generated copies under a Codex home `skills/godogen` directory or a target repository’s `.agents/skills/godogen` directory.

Do not maintain generated `.agents/skills` or `.claude/skills` copies in this source repository.

## Beginner development setup

```bash
python -m venv .venv
```

Activate it:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux or macOS
source .venv/bin/activate
```

Install test dependencies and run the suite:

```bash
python -m pip install --upgrade pip pytest jsonschema
python -m compileall -q skills/godogen/scripts tests
python -m pytest -q
```

## Architecture rules

1. Keep canonical skill source in `skills/godogen`.
2. Treat `.agents/skills` only as an installation destination.
3. Keep environment inspection non-mutating.
4. Refuse filesystem roots, home directories and ambiguous destructive targets.
5. Preserve commands, output, duration and exit codes in proof artifacts.
6. Never turn a failed gate into a pass by suppressing an error.
7. Keep paid asset generation opt-in and auditable.
8. Add tests for every safety or orchestration change.
9. Prefer backward-compatible report schema changes. Increment `schema_version` for breaking changes.
10. Keep Windows, WSL2, Linux and macOS behaviour aligned.

## Adding or changing a command

When adding a command to `skills/godogen/scripts/godogen.py`:

- define its safety boundary;
- return non-zero on material failure;
- write machine-readable output under `artifacts/godogen`;
- preserve human-readable logs;
- add success and failure tests;
- document it in `README.md`;
- update or add a JSON schema when external automation will consume the output.

## Pull request checklist

- The change has a clear player, developer or operator benefit.
- Beginner setup instructions remain copy-ready.
- Advanced behaviour and failure modes are documented.
- Unit tests cover success and failure paths.
- Python compilation passes.
- JSON schemas validate.
- PowerShell parses without errors.
- The diff contains no secrets, generated caches or proof binaries.
- Review findings are answered and resolved.
- CI is green before merge.

## Review priorities

Review data loss and unsafe path handling first. Then check false-positive verification, platform assumptions, hidden spending, secret exposure, dependency drift and claims not backed by executed checks. Style findings come after correctness, recoverability and trustworthy evidence.
