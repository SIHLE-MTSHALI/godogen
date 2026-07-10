# GodoGen installation guide

This guide explains what each dependency does, how to install it and how to verify it before installing the GodoGen skill.

## Windows

The main `README.md` contains the full beginner Windows walkthrough. Use this section when troubleshooting or installing in a different location.

### Required tools

| Tool | Why it is needed | Verification command |
|---|---|---|
| Git | Clone repositories, create branches and preserve history | `git --version` |
| Python 3.10+ | Run GodoGen scripts and tests | `python --version` |
| Godot 4 | Open, import, run and capture the game | `godot --version` |
| .NET SDK | Compile Godot C# projects | `dotnet --version` |
| ffmpeg | Convert and inspect proof media | `ffmpeg -version` |
| Codex | Run the native `$godogen` workflow | `codex --version` when using CLI |

### PATH troubleshooting

PATH is the list of folders Windows searches when you type a command.

To inspect it:

```powershell
$env:Path -split ';'
```

To find a command:

```powershell
Get-Command git
Get-Command python
Get-Command godot
Get-Command dotnet
Get-Command ffmpeg
```

When `Get-Command` cannot find a tool:

1. locate the tool’s executable in File Explorer;
2. copy the containing folder path, not the executable path;
3. search Windows for **Edit environment variables for your account**;
4. edit the user **Path** variable;
5. add the containing folder;
6. confirm the dialogs;
7. close every PowerShell window and open a new one;
8. rerun the version command.

## Linux

The exact package names differ by distribution. The commands below use Ubuntu or Debian.

```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv ffmpeg
```

Install Godot using your distribution package, an official archive or a maintained package manager. C# users need the Godot .NET build and a compatible .NET SDK.

Verify:

```bash
git --version
python3 --version
godot --version
ffmpeg -version
dotnet --version
```

Clone and install the skill for the current user:

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/SIHLE-MTSHALI/godogen.git
mkdir -p ~/.codex/skills
cp -R godogen/skills/godogen ~/.codex/skills/godogen
```

Verify:

```bash
ls ~/.codex/skills/godogen
```

## macOS

Install Homebrew first when it is not already available. Then install the common dependencies:

```bash
brew install git python ffmpeg
```

Install the required Godot edition. C# projects need the .NET edition and .NET SDK.

Verify:

```bash
git --version
python3 --version
godot --version
ffmpeg -version
dotnet --version
```

Install the skill:

```bash
mkdir -p ~/.codex/skills
cp -R skills/godogen ~/.codex/skills/godogen
```

## WSL2

Use WSL2 when your coding tools run in Linux but remember that graphical Godot execution may work better through the native Windows editor.

Check WSL from Windows PowerShell:

```powershell
wsl --status
wsl --list --verbose
```

Inside WSL, install Git, Python and ffmpeg using the Linux steps. Install the skill in the Linux Codex home when Codex runs inside WSL.

Keep repositories in the same environment that performs most file operations. Avoid repeatedly switching between Linux Git and Windows Git on the same checkout.

## Install only for one project

From the GodoGen repository on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\powershell\Install-GodoGen.ps1 -Scope Project -ProjectRoot C:\Projects\MyGame
```

This creates:

```text
C:\Projects\MyGame\.agents\skills\godogen
```

Use project scope when the game requires a pinned skill version or should not depend on a user-wide installation.

## Safe update

Pull the latest fork changes:

```powershell
Set-Location C:\Projects\godogen
git switch master
git pull
```

Reinstall with backup:

```powershell
powershell -ExecutionPolicy Bypass -File .\powershell\Install-GodoGen.ps1 -Scope User -Force
```

## Final diagnostic

From a game repository:

```powershell
python "$HOME\.codex\skills\godogen\scripts\doctor.py" --project . --json artifacts\godogen\doctor.json
```

Open `artifacts/godogen/doctor.json` in a text editor. It should report the operating system, project language, Godot availability, .NET availability and important project settings.
