---
name: godogen
description: Build, continue, repair, test, run, capture, and verify Godot games through a gated Codex-native workflow on Windows, Linux, or macOS.
display_name: GodoGen
default_prompt: Use $godogen to inspect this repository, preserve its working architecture, establish a verified Godot development plan, implement the next working vertical slice, run all build and runtime gates, repair failures, and produce proof artifacts before declaring completion.
allow_implicit_invocation: true
---

# GodoGen native Codex game-development skill

Use this skill for substantive Godot development, including creating a new project, continuing an existing game, adding mechanics, repairing a broken project, improving an existing feature, validating a release, or proving that requested gameplay works.

## Core rule

A clean compile is not completion. Completion requires evidence from the running game.

## Operating contract

1. Read repository instructions, especially `AGENTS.md`, before changing files.
2. Determine whether the task targets a new project or an existing game.
3. Never run bootstrap inside an existing project.
4. Inspect the existing game before changing or scaffolding anything.
5. Preserve the installed Godot version, project language, renderer, physics engine, add-ons, input maps, save formats and repository conventions unless migration is explicitly required.
6. Prefer a playable vertical slice over broad unfinished scaffolding.
7. Keep implementation work and issue or PR administration coupled. Tracking must never replace building.
8. Do not invoke paid asset services without an explicit repository policy or user approval.
9. Never overwrite a non-empty project, delete user content, discard unknown Git changes or rewrite history merely to simplify setup.
10. Keep secrets outside the repository.

## Execution modes

- `safe`: no destructive operation, external spend, dependency replacement or project migration without approval.
- `standard`: autonomous bounded implementation with backups and no paid generation unless approved.
- `full`: high-autonomy implementation, tests, repair, GitHub lifecycle and release verification within stated constraints.

Default to `standard`.

## New project workflow

Use bootstrap only when the target does not already contain a Godot project. Establish the requested language and project shape first. Create the minimal main scene, input configuration, error handling and testable gameplay loop. Prefer procedural placeholders before paid asset generation.

## Existing game workflow

When `project.godot` already exists:

1. Do not bootstrap.
2. Read repository instructions and documentation.
3. Inspect Git status and preserve uncommitted work.
4. Inspect recent commits and open issues when available.
5. Run the environment doctor.
6. Open or safely launch the current game to establish its visible baseline.
7. Map the relevant scenes, scripts, resources, autoloads, input actions, add-ons, tests, save systems and asset conventions.
8. Distinguish existing failures from failures introduced by the task.
9. Record what already works, what is incomplete and what must not be replaced.
10. Select one complete player-visible vertical slice.
11. Implement the smallest coherent change and keep unrelated improvements out of scope.
12. Preserve save compatibility and public interfaces where practical.
13. Add tests with the behaviour.
14. Run every affected downstream gate after each repair.
15. Review the final Git diff for accidental cache, binary, import or unrelated scene changes.

Do not replace working systems merely because a different architecture would be easier to generate.

## Required workflow

### 1. Discover

Run the installed environment doctor:

```bash
python .agents/skills/godogen/scripts/doctor.py --project . --json artifacts/godogen/doctor.json
```

For a user-wide installation, resolve the script from the Codex home instead.

Inspect at minimum:

- `project.godot` and `.csproj` files;
- Godot and .NET versions;
- whether Godot supports C# when required;
- renderer and physics configuration;
- main scene and autoloads;
- input actions;
- add-ons and test frameworks;
- current Git state and recent history;
- existing build, test, capture and export commands;
- save and configuration formats;
- runtime logs and known failures;
- asset directories, import settings and provenance records.

### 2. Plan

Write or update a durable implementation plan. Break work into independently testable vertical slices. Each slice must include:

- player-visible outcome;
- files and systems affected;
- architecture and compatibility constraints;
- acceptance criteria;
- automated checks;
- runtime proof required;
- asset requirements;
- rollback or migration concerns.

Select the highest-value unblocked slice and complete it before starting another.

### 3. Implement

For existing projects:

- follow current architecture and naming;
- make the smallest coherent change;
- avoid replacing working systems without evidence;
- preserve scenes, input mappings, saves and add-on boundaries where practical;
- add tests with behaviour;
- keep the Git diff focused.

For new projects:

- use a Godot-native structure;
- establish one testable gameplay loop first;
- prefer procedural placeholders;
- keep generated assets and provenance in a manifest.

### 4. Build and import

For C# projects:

```bash
dotnet build
godot --headless --path . --import
godot --headless --path . --quit
```

For GDScript projects:

```bash
godot --headless --path . --import
godot --headless --path . --quit
```

Use repository-specific commands when they are more precise. Treat non-zero exits, parser errors, missing resources, invalid UIDs and material runtime errors as failures.

### 5. Test

Run all existing tests. Add tests for deterministic new behaviour. Test at minimum:

- core rules and state transitions;
- scene loading;
- input-independent gameplay logic;
- save and load changes;
- regressions associated with the task.

Do not remove or weaken tests to obtain a passing result.

### 6. Run and capture

Launch the actual game or a deterministic presentation scene. Produce evidence under `artifacts/godogen/`.

The capture must visibly demonstrate the requested mechanic or corrected defect. Avoid static menus, blank frames, repeated identical frames or evidence that omits the relevant gameplay.

### 7. Visual and runtime QA

Inspect for:

- crashes, errors and material warnings;
- missing assets or materials;
- incorrect scale, camera framing, lighting, clipping, collision or animation;
- unreadable or overlapping UI;
- unresponsive controls;
- frame-time regressions;
- visual inconsistency with existing approved assets;
- failure to demonstrate acceptance criteria.

Repair defects and repeat build, test, run and capture until evidence is credible.

### 8. Close out

Before declaring completion:

- ensure the Git diff contains only intended changes;
- update repository status and run instructions;
- document tests and proof artifacts;
- update the asset manifest where relevant;
- state remaining limitations precisely;
- link implemented issues and PRs;
- never claim unexecuted checks as passed.

## Platform policy

Support native Windows, WSL2, Linux and macOS. Prefer native Godot execution when rendering or editor integration is required. Convert paths explicitly when commands cross Windows and WSL boundaries.

On Windows, use the supplied PowerShell installer. Do not require Bash for installation or basic operation.

## Asset policy

Use this priority order:

1. existing repository assets;
2. procedural or code-generated placeholders;
3. user-provided assets;
4. assets manually generated in ChatGPT and supplied through a staging directory;
5. approved local tools such as Blender or ComfyUI;
6. OpenAI image API generation with an approved API key and spending policy;
7. Gemini, xAI, Tripo3D or another approved provider.

### ChatGPT manual asset creation

When a user can create an image in ChatGPT:

1. produce a precise asset brief containing intended use, dimensions, transparency, camera angle, visual style, safe margins and runtime display size;
2. ask the user to generate or approve the image in ChatGPT;
3. place the downloaded file under `artifacts/godogen/asset-staging/`;
4. validate dimensions, alpha, format and visible defects;
5. retain the prompt or brief;
6. import into Godot and inspect the real in-game result;
7. move it into the runtime asset directory only after approval and validation.

### OpenAI API asset creation

When API use is approved:

- read `OPENAI_API_KEY` only from the environment;
- never log or commit the key;
- keep the model name configurable rather than permanently hardcoded;
- enforce approved variation, retry and budget limits;
- save raw outputs to the staging directory;
- preserve the prompt and relevant parameters;
- create unique filenames instead of overwriting variations;
- record a SHA-256 hash;
- report provider errors without secrets;
- stop when acceptance criteria are met or the approved limit is reached.

### All generated assets

Record:

- provider and model or tool;
- source type, such as manual ChatGPT, API, local or user-provided;
- prompt, brief or parameters;
- requested dimensions and transparency;
- licence and provenance notes;
- estimated and actual cost when available;
- staging and runtime paths;
- output hash;
- manual edits;
- intended game usage;
- validation result.

After import, verify Godot settings, runtime display size, transparency edges, materials, texture coordinates, performance and visual consistency. Cache identical requests when the provider workflow supports it.

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

1. preserve the command, exit code and log;
2. identify the smallest plausible cause;
3. apply a bounded repair;
4. rerun the failed gate and every downstream gate;
5. avoid broad dependency upgrades unless required.

After three materially different unsuccessful repair attempts, stop repeating the same approach and produce a focused diagnosis with gathered evidence.
