#!/usr/bin/env python3
"""Inspect a Godot development environment without modifying the project."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def run(command: list[str], cwd: Path) -> dict[str, Any]:
    """Run a bounded diagnostic command and return a serializable result."""
    executable = shutil.which(command[0])
    if executable is None:
        return {
            "command": command,
            "available": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"{command[0]} was not found on PATH",
        }

    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            check=False,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "command": command,
            "available": True,
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc),
        }

    return {
        "command": command,
        "available": True,
        "exit_code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def parse_project(path: Path) -> dict[str, Any]:
    """Read selected project.godot settings without executing the project."""
    if not path.is_file():
        return {"exists": False, "path": str(path)}

    text = path.read_text(encoding="utf-8", errors="replace")
    keys = {
        "application/config/name": None,
        "application/run/main_scene": None,
        "rendering/renderer/rendering_method": None,
        "rendering/renderer/rendering_method.mobile": None,
        "physics/3d/physics_engine": None,
    }
    section = ""
    autoloads: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        if "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        qualified = f"{section}/{key}" if section else key
        if qualified in keys:
            keys[qualified] = value.strip('"')
        if section == "autoload":
            autoloads.append(key)

    return {
        "exists": True,
        "path": str(path),
        "settings": keys,
        "autoloads": sorted(autoloads),
    }


def detect_language(project: Path) -> dict[str, Any]:
    """Infer project languages from source and project files."""
    csproj = sorted(str(path.relative_to(project)) for path in project.glob("*.csproj"))
    csharp = sum(1 for _ in project.rglob("*.cs"))
    gdscript = sum(1 for _ in project.rglob("*.gd"))
    if csharp and gdscript:
        primary = "mixed"
    elif csharp or csproj:
        primary = "csharp"
    elif gdscript:
        primary = "gdscript"
    else:
        primary = "unknown"
    return {
        "primary": primary,
        "csharp_files": csharp,
        "gdscript_files": gdscript,
        "csproj_files": csproj,
    }


def detect_addons(project: Path) -> list[str]:
    """List installed Godot add-on directories."""
    root = project / "addons"
    if not root.is_dir():
        return []
    return sorted(path.name for path in root.iterdir() if path.is_dir())


def version_text(result: dict[str, Any]) -> str | None:
    """Extract the first useful version line from a command result."""
    output = result.get("stdout") or result.get("stderr") or ""
    match = re.search(r"[^\r\n]+", output)
    return match.group(0).strip() if match else None


def build_report(project: Path) -> dict[str, Any]:
    """Build the complete diagnostic report."""
    godot = run(["godot", "--version"], project)
    dotnet = run(["dotnet", "--version"], project)
    git = run(["git", "status", "--short", "--branch"], project)
    ffmpeg = run(["ffmpeg", "-version"], project)

    godot_version = version_text(godot)
    return {
        "schema_version": 1,
        "project_root": str(project),
        "host": {
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "wsl": bool(os.environ.get("WSL_DISTRO_NAME")),
        },
        "project": parse_project(project / "project.godot"),
        "language": detect_language(project),
        "addons": detect_addons(project),
        "tools": {
            "godot": {**godot, "version": godot_version},
            "dotnet": {**dotnet, "version": version_text(dotnet)},
            "git": git,
            "ffmpeg": {**ffmpeg, "version": version_text(ffmpeg)},
        },
        "checks": {
            "is_godot_project": (project / "project.godot").is_file(),
            "godot_available": godot["available"],
            "godot_is_dotnet": bool(
                godot_version
                and any(token in godot_version.lower() for token in ("mono", "dotnet"))
            ),
            "dotnet_available": dotnet["available"],
            "git_clean": git.get("exit_code") == 0
            and not any(
                line and not line.startswith("##")
                for line in git.get("stdout", "").splitlines()
            ),
        },
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".", help="Godot project directory")
    parser.add_argument("--json", dest="json_path", help="Write JSON report here")
    return parser.parse_args()


def main() -> int:
    """Run the environment inspection."""
    args = parse_args()
    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2

    report = build_report(project)
    rendered = json.dumps(report, indent=2, sort_keys=True)

    if args.json_path:
        destination = Path(args.json_path).expanduser()
        if not destination.is_absolute():
            destination = project / destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered + "\n", encoding="utf-8")

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
