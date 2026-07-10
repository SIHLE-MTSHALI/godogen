# GodoGen

GodoGen is an install-once Codex skill and verification toolkit for building, repairing, testing and proving Godot games. It keeps the original project’s strongest principle: a clean compile is not enough. Work is complete only after the running game has produced credible evidence.

The repository still contains the upstream Claude, Bevy and Babylon publishing material, but this fork’s primary path is the native Godot skill under `skills/godogen`.

## What it does

GodoGen gives Codex a repeatable workflow:

1. inspect the machine and existing project;
2. choose a complete, player-visible vertical slice;
3. implement without replacing working systems unnecessarily;
4. build and import the project;
5. run automated tests;
6. launch or record the game;
7. inspect runtime and visual evidence;
8. repair failures and repeat the downstream gates;
9. generate machine-readable proof reports.

It supports Godot C# and GDScript projects on Windows, WSL2, Linux and macOS.

## Beginner quick start on Windows

### 1. Install prerequisites

Install:

- Git;
- Python 3.10 or newer;
- Godot 4;
- the Godot .NET build and .NET SDK when using C#;
- ffmpeg when you want video proof;
- Codex Desktop or Codex CLI.

Make sure `python`, `godot`, `git` and, for C#, `dotnet` work from PowerShell.

### 2. Clone this repository

```powershell
git clone https://github.com/SIHLE-MTSHALI/godogen.git
cd godogen
```

### 3. Install the skill for your user

```powershell
powershell -ExecutionPolicy Bypass -File .\powershell\Install-GodoGen.ps1 -Scope User
```

To replace an older installation safely:

```powershell
powershell -ExecutionPolicy Bypass -File .\powershell\Install-GodoGen.ps1 -Scope User -Force
```

The installer moves the old skill to a timestamped backup before copying the new version.

### 4. Verify a Godot project

From the game repository, ask Codex:

```text
$godogen inspect this project, explain what is working and broken, implement the next complete gameplay slice, run every required gate, repair failures and produce proof artifacts.
```

You can also run the tools directly from the installed skill:

```powershell
python "$HOME\.codex\skills\godogen\scripts\doctor.py" --project . --json artifacts\godogen\doctor.json
python "$HOME\.codex\skills\godogen\scripts\godogen.py" build --project .
python "$HOME\.codex\skills\godogen\scripts\godogen.py" test --project .
python "$HOME\.codex\skills\godogen\scripts\godogen.py" verify --project .
```

## Create a starter project

GDScript:

```powershell
python skills\godogen\scripts\godogen.py bootstrap C:\Games\MyGame --name MyGame --language gdscript
```

C#:

```powershell
python skills\godogen\scripts\godogen.py bootstrap C:\Games\MyGame --name MyGame --language csharp
```

Bootstrap refuses unsafe and non-empty destinations by default. It writes `artifacts/godogen/bootstrap-manifest.json`, listing every file it created.

## Command reference

| Command | Purpose | Main output |
|---|---|---|
| `doctor.py` | Non-mutating environment and project inspection | `doctor.json` |
| `godogen.py bootstrap` | Create a minimal safe Godot project | bootstrap manifest |
| `godogen.py build` | Build C#, import resources and smoke-load Godot | build report and logs |
| `godogen.py test` | Run GUT, .NET tests or a smoke fallback | test report and log |
| `godogen.py capture` | Record deterministic proof using Godot movie writing | video and capture report |
| `godogen.py verify` | Check required reports and hash evidence | proof report and summary |

Run `python skills/godogen/scripts/godogen.py --help` for all options.

## Evidence directory

GodoGen writes generated evidence under:

```text
artifacts/godogen/
├── doctor.json
├── bootstrap-manifest.json
├── build-report.json
├── test-report.json
├── capture-report.json
├── proof-report.json
├── proof-summary.md
├── *.log
├── screenshots/
└── video/
```

`proof-report.json` follows `skills/godogen/schemas/proof-report.schema.json` and includes SHA-256 hashes for the evidence files.

## Safety model

- The canonical skill source lives in `skills/godogen`, not `.agents/skills`.
- `.agents/skills/godogen` is only a project-scoped installation destination.
- The Windows installer supports `-WhatIf` and safe backup-on-replace.
- Bootstrap refuses filesystem roots, home directories and shallow unsafe targets.
- Existing project files are not overwritten by bootstrap.
- Paid asset providers are never invoked unless repository policy or the user explicitly approves the spend.
- Secrets remain outside the repository.

## Advanced workflow

The skill defines `safe`, `standard` and `full` modes. Standard mode is the default. In all modes, Codex must inspect `AGENTS.md`, preserve the existing Godot version and architecture where practical, implement one coherent vertical slice at a time, and rerun every downstream gate after a repair.

For C# projects, GodoGen runs `dotnet build` before Godot import and smoke loading. For GDScript projects it imports and smoke-loads directly. Existing project-specific commands take precedence when they are more precise.

Capture is intentionally separate from build and test because graphical execution may require a native desktop, GPU, display server or project-specific presentation scene. Use `verify --require-capture` only when a capture has actually been produced.

## Repository layout

```text
skills/godogen/                 Canonical Codex skill source
powershell/Install-GodoGen.ps1  Windows installer
tests/                          Python tool tests
.github/workflows/              Cross-platform CI
asset-gen/                      Upstream asset generation system
engines/                        Upstream engine guidance
publish.sh                      Legacy/upstream publisher
```

## Development and validation

```bash
python -m pip install pytest
python -m compileall -q skills/godogen/scripts tests
python -m pytest -q
```

CI runs on Windows, Ubuntu and macOS with Python 3.10 and 3.12. It validates skill metadata, Python syntax, unit tests, JSON schemas and PowerShell parsing.

## Troubleshooting

### `godot` is not found

Add the directory containing the Godot executable to `PATH`, restart the terminal and run `godot --version`.

### C# project reports that Godot is not a .NET build

Install the Godot .NET edition. The standard editor cannot compile or run Godot C# scripts.

### The installer says GodoGen already exists

Run it with `-Force`. The existing installation is moved to a timestamped backup first.

### Capture produces no useful video

Confirm the project has a main scene, renders on the current machine and exits within the selected frame count. For deterministic proof, create a presentation scene that drives input and camera movement itself.

### Verification fails with missing reports

Run `build` and `test` first. Add `capture`, then use `verify --require-capture`, only when visual proof is part of the acceptance criteria.

## Status

This fork is focused on the native Godot/Codex workflow. The legacy multi-engine publisher remains available for compatibility, but new Codex-oriented development should use the installed `$godogen` skill.

See `CHANGELOG.md` for release history and `CONTRIBUTING.md` for contribution standards.
