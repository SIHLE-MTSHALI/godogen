import importlib.util
import json
from pathlib import Path


SCRIPT = Path('skills/godogen/scripts/openai_asset.py')
spec = importlib.util.spec_from_file_location('openai_asset', SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_safe_name():
    assert module.safe_name('Plasma Rifle Icon V02') == 'plasma-rifle-icon-v02'


def test_append_manifest(tmp_path):
    path = tmp_path / 'asset-manifest.json'
    module.append_manifest(path, {'id': 'one'})
    module.append_manifest(path, {'id': 'two'})
    data = json.loads(path.read_text(encoding='utf-8'))
    assert data['schema_version'] == 1
    assert [item['id'] for item in data['assets']] == ['one', 'two']


def test_sha256(tmp_path):
    path = tmp_path / 'asset.png'
    path.write_bytes(b'asset')
    assert len(module.sha256(path)) == 64
