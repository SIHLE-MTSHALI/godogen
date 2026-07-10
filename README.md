# GodoGen

GodoGen is an install-once Codex skill and verification toolkit for building, repairing, testing and proving Godot games. It works with new projects and games that already contain code, scenes, assets, tests and Git history.

The main rule is simple: a clean compile is not enough. Work is complete only after the requested behaviour has been tested in the running game and supported by evidence.

## Choose the path that matches your situation

- **You have never installed Godot, Git, Python or Codex:** start at [Complete Windows setup for beginners](#complete-windows-setup-for-beginners).
- **You want to create a new game:** complete installation, then follow [Create a new game](#create-a-new-game).
- **You already have a Godot game:** complete installation, then follow [Continue working on an existing game](#continue-working-on-an-existing-game).
- **You want generated game art:** read [Asset creation options](#asset-creation-options) and the detailed [asset guide](docs/ASSET_CREATION.md).
- **You use Linux, macOS or WSL2:** read [Cross-platform installation](docs/INSTALLATION.md).

## What GodoGen does

GodoGen gives Codex a repeatable workflow:

1. inspect the computer and repository;
2. understand the current game before changing it;
3. choose one complete player-visible improvement;
4. make the smallest coherent implementation;
5. build and import the project;
6. run tests;
7. launch or record the game;
8. inspect runtime and visual evidence;
9. repair failures and repeat affected checks;
10. produce machine-readable proof reports.

It supports Godot C# and GDScript projects on Windows, WSL2, Linux and macOS.

# Complete Windows setup for beginners

The steps below assume Windows 10 or Windows 11 and no previous development setup.

## Step 1: Open PowerShell

1. Press the **Windows key**.
2. Type **PowerShell**.
3. Open **Windows PowerShell** or **PowerShell**.
4. A blue or black command window will appear. Commands in this guide are pasted into that window.

You do not need Administrator mode for the normal installation path.

## Step 2: Install Git

Git downloads repositories and records every code change.

1. Open a web browser.
2. Go to the official Git for Windows website: `https://git-scm.com/download/win`.
3. Download the 64-bit installer.
4. Run the installer.
5. Keep the default selections unless your organisation requires different settings.
6. When asked about the PATH option, keep the option that allows Git to be used from the command line and third-party software.
7. Finish the installation.
8. Close PowerShell and open it again.
9. Verify Git:

```powershell
git --version
```

A successful result resembles:

```text
git version 2.x.x.windows.x
```

If PowerShell says `git is not recognized`, restart Windows. If the problem remains, reinstall Git and make sure command-line PATH integration is selected.

## Step 3: Install Python

GodoGen uses Python for its doctor, build orchestration and proof reports.

1. Open `https://www.python.org/downloads/windows/`.
2. Download the latest supported Python 3 installer. Python 3.10 or newer is required.
3. Run the installer.
4. On the first installer screen, tick **Add python.exe to PATH**.
5. Select **Install Now**.
6. Finish the installation.
7. Close and reopen PowerShell.
8. Verify Python:

```powershell
python --version
```

A successful result resembles:

```text
Python 3.12.x
```

Also verify pip:

```powershell
python -m pip --version
```

If `python` opens the Microsoft Store or is not recognised, open **Settings**, search for **App execution aliases**, and disable the `python.exe` and `python3.exe` Store aliases. Reopen PowerShell and try again.

## Step 4: Install Godot

Choose the correct Godot edition for your project.

### For GDScript projects

Install the standard Godot 4 Windows build.

### For C# projects

Install the Godot 4 **.NET** build. The standard build cannot compile or run C# scripts.

Installation steps:

1. Open `https://godotengine.org/download/windows/`.
2. Download the required Windows build.
3. Extract the downloaded ZIP file.
4. Create a permanent folder such as:

```text
C:\Tools\Godot
```

5. Move the extracted Godot executable and its supporting files into that folder.
6. Rename the executable to `godot.exe` to make command-line use simpler.
7. Add `C:\Tools\Godot` to your user PATH:
   1. Press the Windows key.
   2. Search for **Edit environment variables for your account**.
   3. Open it.
   4. Select the user variable named **Path**.
   5. Select **Edit**.
   6. Select **New**.
   7. Enter `C:\Tools\Godot`.
   8. Confirm all open dialogs.
8. Close and reopen PowerShell.
9. Verify Godot:

```powershell
godot --version
```

For a C# installation, the version output should identify a .NET or Mono-capable build.

## Step 5: Install the .NET SDK for C# games

Skip this step when your game uses only GDScript.

1. Open `https://dotnet.microsoft.com/download`.
2. Download the current supported .NET SDK for Windows x64.
3. Run the installer using the default options.
4. Close and reopen PowerShell.
5. Verify it:

```powershell
dotnet --version
```

The command should return a version number. An SDK is required, not only a runtime.

## Step 6: Install ffmpeg for proof video

GodoGen can build and test without ffmpeg, but video conversion and some asset workflows require it.

The simplest beginner installation uses Windows Package Manager:

```powershell
winget install --id Gyan.FFmpeg -e
```

Close and reopen PowerShell, then verify:

```powershell
ffmpeg -version
```

If `winget` is unavailable, install or update **App Installer** from Microsoft Store, then run the command again.

## Step 7: Install Codex

Use the Codex product you already use for repository work. Confirm that it can open a local folder and run terminal commands. When using Codex CLI, verify it from PowerShell:

```powershell
codex --version
```

When Codex is installed but the command is not recognised, reopen the terminal after installation and confirm its installation directory was added to PATH.

## Step 8: Verify all prerequisites together

Run each command separately:

```powershell
git --version
python --version
python -m pip --version
godot --version
ffmpeg -version
```

For a C# game, also run:

```powershell
dotnet --version
```

Do not continue until every required command returns a version instead of an error.

## Step 9: Download GodoGen

Choose a parent folder for development repositories. This example uses `C:\Projects`.

```powershell
New-Item -ItemType Directory -Path C:\Projects -Force
Set-Location C:\Projects
git clone https://github.com/SIHLE-MTSHALI/godogen.git
Set-Location .\godogen
```

Confirm you are in the correct repository:

```powershell
Get-ChildItem
```

You should see files such as `README.md`, `skills`, `powershell` and `tests`.

## Step 10: Install the skill

Install it for your Windows user so it is available from any game repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\powershell\Install-GodoGen.ps1 -Scope User
```

The default installation location is:

```text
C:\Users\YOUR_USERNAME\.codex\skills\godogen
```

Verify the copied files:

```powershell
Get-ChildItem "$HOME\.codex\skills\godogen"
```

You should see `SKILL.md`, `agents`, `scripts` and `schemas`.

To safely replace an older installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\powershell\Install-GodoGen.ps1 -Scope User -Force
```

The previous installation is moved to a timestamped backup before replacement.

# Create a new game

Choose a folder that does not already contain files.

## GDScript example

```powershell
python "$HOME\.codex\skills\godogen\scripts\godogen.py" bootstrap C:\Projects\MyGame --name MyGame --language gdscript
Set-Location C:\Projects\MyGame
```

## C# example

```powershell
python "$HOME\.codex\skills\godogen\scripts\godogen.py" bootstrap C:\Projects\MyGame --name MyGame --language csharp
Set-Location C:\Projects\MyGame
```

Bootstrap refuses unsafe or non-empty destinations by default and writes a manifest listing the files it created.

Open the project in Godot:

```powershell
godot --editor --path .
```

Open the same folder in Codex and use:

```text
$godogen inspect this new project, confirm the toolchain works, propose the first small playable vertical slice, implement it, test it and produce proof artifacts.
```

# Continue working on an existing game

Do not run `bootstrap` inside an existing project. GodoGen must inspect and preserve the project that already exists.

## Case A: The game is already on your computer

1. Make sure you know the folder containing `project.godot`.
2. Open PowerShell.
3. Change into that folder. Example:

```powershell
Set-Location C:\Projects\ExistingGame
```

4. Confirm the project file exists:

```powershell
Test-Path .\project.godot
```

The result must be `True`.

5. Check the repository state:

```powershell
git status
```

When the folder is not yet a Git repository, create one before allowing major changes:

```powershell
git init
git add .
git commit -m "Baseline existing game before GodoGen"
```

When Git asks for your name or email, configure them once:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

6. When `git status` shows uncommitted work you want to preserve, commit it before continuing:

```powershell
git add .
git commit -m "Save current work before GodoGen changes"
```

7. Create a working branch:

```powershell
git switch -c feature/godogen-next-slice
```

8. Run the non-mutating doctor:

```powershell
python "$HOME\.codex\skills\godogen\scripts\doctor.py" --project . --json artifacts\godogen\doctor.json
```

9. Open the folder in Codex and use this first request:

```text
$godogen inspect this existing game without replacing its architecture. Read AGENTS.md, README files, project.godot, scenes, scripts, add-ons, tests and Git history. Explain what already works, what is incomplete or broken, and the safest next complete player-visible vertical slice. Do not change files until the assessment and plan are recorded.
```

10. After the assessment, use:

```text
$godogen implement the selected vertical slice. Preserve existing working systems, add or update tests, run build and import checks, launch the game, repair failures and produce proof artifacts. Do not broaden the scope until this slice is complete.
```

## Case B: The game is stored on GitHub

1. Open the repository page in your browser.
2. Select the green **Code** button.
3. Copy the HTTPS repository address.
4. In PowerShell, choose a parent directory and clone it:

```powershell
Set-Location C:\Projects
git clone YOUR_REPOSITORY_URL
Set-Location .\YOUR_REPOSITORY_FOLDER
```

5. Confirm that `project.godot` exists and run `git status`.
6. Create a new branch before changes:

```powershell
git switch -c feature/godogen-next-slice
```

7. Follow steps 8 to 10 from Case A.

## Existing-project rules

GodoGen must:

- inspect before scaffolding;
- preserve the installed Godot version and project language;
- preserve working scenes, scripts, input maps, save formats and add-ons unless migration is explicitly required;
- use the project’s existing build and test commands when they are more specific;
- implement one complete vertical slice at a time;
- never overwrite existing files merely to simplify implementation;
- keep the Git diff focused;
- rerun all affected downstream checks after repairs;
- document remaining limitations honestly.

The full existing-game guide is in [docs/EXISTING_PROJECTS.md](docs/EXISTING_PROJECTS.md).

# Asset creation options

GodoGen can use several asset sources. Existing project assets and procedural placeholders remain the first choices because they are fast, cheap and easy to replace.

Supported paths include:

1. existing repository assets;
2. procedural or code-generated placeholders;
3. assets supplied by the user;
4. assets created manually in ChatGPT and added to the repository;
5. assets generated through the OpenAI image API when an approved API key and budget policy exist;
6. approved local tools such as Blender or ComfyUI;
7. Gemini, xAI, Tripo3D and other approved providers.

## Using ChatGPT manually for assets

Ask ChatGPT to create a specific game asset, including exact dimensions, camera angle, background requirements and visual style. Download the resulting image and place it in a staging folder such as:

```text
artifacts/godogen/asset-staging/
```

Then tell Codex the file path and intended use. GodoGen must validate dimensions, transparency, file format, naming and Godot import behaviour before moving it into the runtime asset directory.

## Using OpenAI through an API

API generation is a paid external action. GodoGen must not call it until the user or repository policy approves the provider and spending limit. The API key must be supplied through an environment variable and must never be committed.

Generated assets must record:

- provider and model or tool;
- prompt and generation parameters;
- requested dimensions and transparency;
- creation date;
- estimated and actual cost when available;
- output file hash;
- intended game usage;
- licence or provenance notes;
- any manual edits after generation.

Read [docs/ASSET_CREATION.md](docs/ASSET_CREATION.md) for complete ChatGPT, OpenAI API and alternative-provider workflows.

# Command reference

| Command | Purpose | Main output |
|---|---|---|
| `doctor.py` | Non-mutating environment and project inspection | `doctor.json` |
| `godogen.py bootstrap` | Create a minimal safe Godot project | bootstrap manifest |
| `godogen.py build` | Build C#, import resources and smoke-load Godot | build report and logs |
| `godogen.py test` | Run GUT, .NET tests or a smoke fallback | test report and log |
| `godogen.py capture` | Record deterministic proof using Godot movie writing | video and capture report |
| `godogen.py verify` | Check required reports and hash evidence | proof report and summary |

Run:

```powershell
python "$HOME\.codex\skills\godogen\scripts\godogen.py" --help
```

# Evidence directory

```text
artifacts/godogen/
├── doctor.json
├── bootstrap-manifest.json
├── build-report.json
├── test-report.json
├── capture-report.json
├── proof-report.json
├── proof-summary.md
├── asset-staging/
├── asset-manifest.json
├── *.log
├── screenshots/
└── video/
```

# Safety model

- Canonical skill source lives in `skills/godogen`.
- `.agents/skills/godogen` is only a project installation destination.
- The installer supports `-WhatIf` and backup-on-replace.
- Bootstrap refuses roots, home directories and shallow unsafe targets.
- Existing project files are not overwritten by bootstrap.
- Existing games are inspected, branched and baselined before substantive changes.
- Paid asset generation requires explicit approval or repository policy.
- Secrets remain outside the repository.

# Development and validation

```powershell
python -m pip install pytest jsonschema
python -m compileall -q skills\godogen\scripts tests
python -m pytest -q
```

CI runs on Windows, Ubuntu and macOS using Python 3.10 and 3.12.

# Troubleshooting

Detailed troubleshooting is included in [docs/INSTALLATION.md](docs/INSTALLATION.md). Common checks are:

```powershell
git --version
python --version
godot --version
ffmpeg -version
dotnet --version
```

When one command is not recognised, close and reopen PowerShell first. Then check the PATH instructions for that tool.

# Status

This fork focuses on the native Godot and Codex workflow. The legacy multi-engine publisher remains for compatibility, but new Codex-oriented development should use the installed `$godogen` skill.

See `CONTRIBUTING.md` for development standards.
