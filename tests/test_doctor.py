"""Tests for the native GodoGen environment doctor."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


DOCTOR_PATH = (
    Path(__file__).parents[1]
    / ".agents"
    / "skills"
    / "godogen"
    / "scripts"
    / "doctor.py"
)


def load_doctor():
    """Load doctor.py directly from the native skill directory."""
    spec = importlib.util.spec_from_file_location("godogen_doctor", DOCTOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_missing_project(tmp_path: Path) -> None:
    """A missing project.godot must be represented, not treated as a crash."""
    doctor = load_doctor()
    result = doctor.parse_project(tmp_path / "project.godot")
    assert result["exists"] is False


def test_parse_project_settings_and_autoloads(tmp_path: Path) -> None:
    """Selected version-sensitive settings and autoloads are extracted."""
    project_file = tmp_path / "project.godot"
    project_file.write_text(
        """; Engine configuration file.
[application]
config/name="Test Game"
run/main_scene="res://scenes/main.tscn"

[autoload]
GameState="*res://scripts/game_state.gd"

[physics]
3d/physics_engine="Jolt Physics"

[rendering]
renderer/rendering_method="gl_compatibility"
""",
        encoding="utf-8",
    )

    doctor = load_doctor()
    result = doctor.parse_project(project_file)

    assert result["exists"] is True
    assert result["settings"]["application/config/name"] == "Test Game"
    assert result["settings"]["application/run/main_scene"] == (
        "res://scenes/main.tscn"
    )
    assert result["settings"]["physics/3d/physics_engine"] == "Jolt Physics"
    assert result["autoloads"] == ["GameState"]


def test_detect_language(tmp_path: Path) -> None:
    """Mixed C# and GDScript projects are identified explicitly."""
    (tmp_path / "Game.csproj").write_text("<Project />", encoding="utf-8")
    (tmp_path / "player.cs").write_text("class Player {}", encoding="utf-8")
    (tmp_path / "enemy.gd").write_text("extends Node", encoding="utf-8")

    doctor = load_doctor()
    result = doctor.detect_language(tmp_path)

    assert result["primary"] == "mixed"
    assert result["csharp_files"] == 1
    assert result["gdscript_files"] == 1
    assert result["csproj_files"] == ["Game.csproj"]


def test_report_is_json_serializable(tmp_path: Path) -> None:
    """The complete report must remain machine-readable on partial systems."""
    doctor = load_doctor()
    report = doctor.build_report(tmp_path)
    rendered = json.dumps(report)

    assert rendered
    assert report["schema_version"] == 1
    assert report["checks"]["is_godot_project"] is False
