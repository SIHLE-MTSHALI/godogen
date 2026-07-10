---
name: godogen
description: Build, repair, test, run, capture, and verify Godot games through a gated Codex-native workflow on Windows, Linux, or macOS.
display_name: GodoGen
default_prompt: Use $godogen to inspect this repository, establish a verified Godot development plan, implement the next working vertical slice, run all build and runtime gates, repair failures, and produce proof artifacts before declaring completion.
allow_implicit_invocation: true
---

# GodoGen — native Codex game-development skill

Use this skill for substantive Godot game development: creating a project, adding mechanics, repairing a broken project, improving an existing game, validating a release, or proving that requested gameplay works.

## Core rule

A clean compile is not completion. Completion requires evidence from the running game.

## Operating contract

1. Read repository instructions, especially `AGENTS.md`, before changing files.
2. Inspect the existing project before scaffolding anything.
3. Preserve the installed Godot version, project language, renderer, physics engine, add-ons, and repository conventions unless the task explicitly requires migration.
4. Prefer a playable vertical slice over broad unfinished scaffolding.
5. Keep implementation work and issue/PR administration coupled. Tracking work must never replace building the product.
6. Do not invoke paid asset services without an explicit repository policy or user approval.
7. Never overwrite a non-empty project, delete user content, or rewrite Git history merely to simplify setup.
8. Keep secrets outside the repository.

## Execution modes

Determine the mode from repository policy or task wording:

- `safe`: no destructive operation, external spend, dependency replacement, or project migration without approval.
- `standard`: autonomous implementation with bounded changes, backups for generated replacements, and no paid generation unless pre-approved.
- `full`: high-autonomy implementation, test, repair, GitHub lifecycle, and release verification within stated constraints.

Default to `standard`.

## Required workflow

### 1. Discover

Run the environment doctor:

```bash
python .agents/skills/godogen/scripts/doctor.py --project . --json artifacts/godogen/doctor.json
```

Inspect at minimum:

- `project.godot` and any `.csproj` files;
- Godot and .NET versions;
- whether the installed Godot build supports C#;
- renderer and physics configuration;
- main scene and autoloads;
- add-ons and test frameworks;
- current Git status;
- existing build, test, capture, and export commands;
- runtime logs and known failures.

If the repository is not yet a Godot project, record that explicitly and scaffold only after establishing the requested language and project shape.

### 2. Plan

Write or update a durable implementation plan in the repository. Break work into independently testable vertical slices. Each slice must include:

- player-visible outcome;
- files or systems affected;
- acceptance criteria;
- automated checks;
- runtime proof required;
- rollback or migration concerns.

Select the highest-value unblocked slice and implement it fully before moving to another.

### 3. Implement

For existing projects:

- follow current architecture and naming;
- make the smallest coherent change that satisfies the slice;
- avoid replacing working systems without evidence;
- preserve compatibility with current saves and scenes where practical;
- add tests with the behaviour.

For new projects:

- use Godot-native project structure;
- establish input actions, main scene, error handling, and a minimal testable gameplay loop first;
- prefer procedural placeholders before external asset generation;
- keep generated assets and their provenance in a manifest.

### 4. Build and import

Use the project language:

**C# projects**

```bash
dotnet build
godot --headless --path . --import
godot --headless --path . --quit
```

**GDScript projects**

```bash
godot --headless --path . --import
godot --headless --path . --quit
```

Use the repository's own commands where they are more specific. Treat non-zero exits, parser errors, missing resources, invalid UIDs, and material runtime errors as failures.

### 5. Test

Run all existing tests. Add tests for new deterministic behaviour. Test at minimum:

- core rules and state transitions;
- scene loading;
- input-independent gameplay logic;
- save/load changes where relevant;
- regressions associated with the task.

Do not remove or weaken tests to obtain a passing result.

### 6. Run and capture

Launch the actual game or a deterministic presentation/test scene. Produce evidence under:

```text
artifacts/godogen/
├── doctor.json
├── build.log
├── runtime.log
├── test-results.*
├── screenshots/
├── video/
└── proof-summary.md
```

The capture must visibly demonstrate the requested mechanic or corrected defect. Avoid static menus, blank frames, repeated identical frames, or captures that omit the relevant gameplay.

### 7. Visual and runtime QA

Inspect the captured result for:

- crashes, errors, warnings with material impact;
- missing assets or materials;
- incorrect scale, camera framing, lighting, clipping, collision, or animation;
- unreadable or overlapping UI;
- unresponsive controls;
- frame-time regressions;
- failure to demonstrate the acceptance criteria.

Repair defects and repeat build, test, run, and capture until the evidence is credible.

### 8. Close out

Before declaring completion:

- ensure Git diff contains only intended changes;
- update repository status and run instructions;
- document tests and proof artifacts;
- state remaining limitations precisely;
- link implemented issues and PRs where applicable;
- never claim unexecuted checks as passed.

## Platform policy

Support native Windows, WSL2, Linux, and macOS. Prefer native Godot execution when rendering or editor integration is required. Convert paths explicitly when commands cross Windows and WSL boundaries.

On Windows, use PowerShell scripts supplied by this skill. Do not require Bash for installation or basic operation.

## Asset policy

Use this priority order:

1. existing repository assets;
2. procedural or local placeholders;
3. user-provided assets;
4. approved local generation tools;
5. approved paid providers.

For generated assets, record provider, model/tool, source prompt or parameters, licence/provenance, estimated cost, actual cost when known, and output hash. Cache identical requests.

## Godot-specific safeguards

- Match version-sensitive SDK and project settings to the installed toolchain.
- Do not guess C# API names when assemblies or documentation can be inspected.
- Ensure generated scene ownership is valid before saving packed scenes.
- Do not recurse ownership into imported GLB or nested scene resources.
- Validate packed scenes by instantiating them after save.
- Use primitive collision approximations for complex imported meshes unless profiling justifies otherwise.
- Do not place `.gdignore` in runtime asset directories.
- Keep movement and damping frame-rate independent.

## Failure handling

When a gate fails:

1. preserve the relevant command, exit code, and log;
2. identify the smallest plausible cause;
3. apply a bounded repair;
4. rerun the failed gate and all downstream gates;
5. avoid broad dependency upgrades unless the failure requires them.

After three materially different unsuccessful repair attempts, stop repeating the same approach and produce a focused diagnosis with the evidence gathered.