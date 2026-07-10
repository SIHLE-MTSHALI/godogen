import importlib.util
import json
from pathlib import Path


SCRIPT = Path('skills/godogen/scripts/godogen.py')
spec = importlib.util.spec_from_file_location('godogen_cli', SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_project_language(tmp_path):
    (tmp_path / 'project.godot').write_text('config_version=5\n', encoding='utf-8')
    assert module.project_language(tmp_path) == 'unknown'
    (tmp_path / 'main.gd').write_text('extends Node\n', encoding='utf-8')
    assert module.project_language(tmp_path) == 'gdscript'
    (tmp_path / 'Game.csproj').write_text('<Project />\n', encoding='utf-8')
    assert module.project_language(tmp_path) == 'csharp'


def test_bootstrap_creates_manifest(tmp_path):
    target = tmp_path / 'games' / 'demo'
    args = type('Args', (), {'target': str(target), 'allow_non_empty': False, 'name': 'Demo Game', 'language': 'gdscript'})()
    assert module.bootstrap(args) == 0
    assert (target / 'project.godot').is_file()
    assert (target / 'scripts/main.gd').is_file()
    manifest = json.loads((target / 'artifacts/godogen/bootstrap-manifest.json').read_text(encoding='utf-8'))
    assert manifest['operation'] == 'bootstrap'
    assert manifest['language'] == 'gdscript'


def test_verify_fails_without_reports(tmp_path):
    (tmp_path / 'project.godot').write_text('config_version=5\n', encoding='utf-8')
    args = type('Args', (), {'project': str(tmp_path), 'timeout': 1, 'require_capture': False})()
    assert module.verify(args) == 1
    report = json.loads((tmp_path / 'artifacts/godogen/proof-report.json').read_text(encoding='utf-8'))
    assert report['status'] == 'failed'
    assert len(report['failures']) == 2


def test_verify_passes_with_required_reports(tmp_path):
    (tmp_path / 'project.godot').write_text('config_version=5\n', encoding='utf-8')
    artifact = tmp_path / 'artifacts/godogen'
    artifact.mkdir(parents=True)
    for name in ('build-report.json', 'test-report.json'):
        (artifact / name).write_text(json.dumps({'schema_version': 1, 'status': 'passed'}), encoding='utf-8')
    args = type('Args', (), {'project': str(tmp_path), 'timeout': 1, 'require_capture': False})()
    assert module.verify(args) == 0
    report = json.loads((artifact / 'proof-report.json').read_text(encoding='utf-8'))
    assert report['status'] == 'passed'
    assert report['artifact_sha256']
