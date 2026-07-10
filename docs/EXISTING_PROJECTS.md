# Continue an existing Godot game with GodoGen

This guide is for projects that already contain `project.godot`, scenes, scripts or assets. The goal is to continue the game without replacing working systems or losing history.

## 1. Confirm the project folder

Open PowerShell and move into the folder that contains `project.godot`:

```powershell
Set-Location C:\Projects\ExistingGame
Test-Path .\project.godot
```

Continue only when the result is `True`.

## 2. Open the game before changing it

Run the editor:

```powershell
godot --editor --path .
```

Start the game from Godot. Record obvious problems, missing assets, broken controls or incomplete features. This establishes the visible baseline.

## 3. Protect current work with Git

Check Git status:

```powershell
git status
```

### The folder is not a Git repository

Create a repository and save the baseline:

```powershell
git init
git add .
git commit -m "Baseline existing game before GodoGen"
```

### The repository has uncommitted changes

Inspect the listed files. Commit wanted work:

```powershell
git add .
git commit -m "Save current work before GodoGen changes"
```

Do not discard unknown changes merely to obtain a clean status.

## 4. Create a dedicated working branch

```powershell
git switch -c feature/godogen-next-slice
```

A branch keeps experimental changes separate from the stable branch and makes review or rollback easier.

## 5. Run the environment doctor

```powershell
python "$HOME\.codex\skills\godogen\scripts\doctor.py" --project . --json artifacts\godogen\doctor.json
```

Review the report for:

- Godot version;
- whether the project is C#, GDScript or mixed;
- .NET availability for C#;
- renderer and physics engine;
- main scene;
- autoloads;
- installed add-ons;
- Git cleanliness.

## 6. Ask Codex for assessment before implementation

Use this request:

```text
$godogen assess this existing game before changing it. Read all repository instructions, project.godot, C# project files, scenes, scripts, resources, input actions, autoloads, add-ons, tests, documentation, open issues and recent Git history. Run the non-mutating doctor and existing safe checks. Explain what currently works, what is incomplete, what is broken, the architecture that must be preserved, and the safest next complete player-visible vertical slice. Record the plan before implementation.
```

A good assessment should identify concrete evidence rather than guessing from filenames.

## 7. Select one vertical slice

A vertical slice is a complete improvement a player can see or use. Examples:

- the player can pick up one weapon, fire it, damage one enemy and see ammunition on the HUD;
- the main menu can start a new game and return from gameplay;
- one enemy can detect, chase and attack the player;
- one save slot can store and restore position and inventory;
- one level can be entered, completed and exited.

Avoid broad tasks such as "finish combat" or "improve everything". Those produce many partially connected systems and weak verification.

## 8. Implement without replacing the project

Use:

```text
$godogen implement the selected vertical slice in this existing game. Preserve current architecture, scenes, input mappings, save compatibility, add-ons and working behaviour. Make the smallest coherent change, add or update tests, document new assets and dependencies, run all build and import gates, launch the game, repair failures and produce proof artifacts. Keep unrelated improvements out of this branch.
```

The skill must not run bootstrap inside the existing project.

## 9. Review changes during the work

Use Git to see changed files:

```powershell
git status
git diff --stat
git diff
```

Check for accidental changes to imported caches, generated binaries, local settings or unrelated scenes.

## 10. Run deterministic gates

```powershell
python "$HOME\.codex\skills\godogen\scripts\godogen.py" build --project .
python "$HOME\.codex\skills\godogen\scripts\godogen.py" test --project .
```

When visual proof is required:

```powershell
python "$HOME\.codex\skills\godogen\scripts\godogen.py" capture --project .
python "$HOME\.codex\skills\godogen\scripts\godogen.py" verify --project . --require-capture
```

Otherwise:

```powershell
python "$HOME\.codex\skills\godogen\scripts\godogen.py" verify --project .
```

## 11. Review the result in Godot

Open the editor and play the game again:

```powershell
godot --editor --path .
```

Confirm the requested behaviour, controls, UI, collisions, audio and scene transitions. A generated video is evidence, but it does not replace direct review when you are available.

## 12. Commit and open a pull request

```powershell
git add .
git commit -m "Complete selected gameplay slice"
git push -u origin feature/godogen-next-slice
```

Open a pull request and include:

- the player-visible result;
- changed systems;
- tests run;
- proof artifact locations;
- known limitations;
- screenshots or video when useful.

## Existing game preservation checklist

Before merging, confirm:

- working features still behave correctly;
- no existing scenes or scripts were replaced without a clear need;
- input actions were preserved or deliberately migrated;
- save formats remain compatible or include migration handling;
- add-ons were not upgraded unnecessarily;
- asset import settings are intentional;
- tests were not weakened;
- warnings with material runtime impact are resolved;
- the diff contains only the selected slice;
- the README or project status reflects the new state.

## Special situations

### The game has no tests

Add tests for deterministic logic introduced by the slice. Use a smoke launch for scene loading and direct gameplay proof for behaviour that cannot be tested headlessly.

### The game is already broken

Separate baseline failures from new failures. Record existing failures before editing. The selected task may fix them, but the final report must not claim unrelated baseline defects were introduced by the new work.

### The project is very large

Read repository instructions and architecture documents first. Limit search to the relevant subsystem, then trace dependencies before changing shared autoloads, save systems, input infrastructure or base scenes.

### The project uses mixed C# and GDScript

Preserve the existing boundary. Do not rewrite one language into the other unless migration is the explicit task and has dedicated tests and rollback planning.
