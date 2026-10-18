"""Verify archived bytes and disallow local configuration in public paths."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'archive/manifest.json').read_text(encoding='utf-8'))
for item in manifest:
    path=root/item['published']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'], str(path)
for area in ['archive','simulation','data','src','docs','tests','tools','.github']:
    for path in (root/area).rglob('*'):
        if path.is_file():
            assert path.name not in {'.env','runtpe','profiles.yml'}, str(path)
            assert path.stat().st_size<5_000_000, str(path)
print(f'PASS: {len(manifest)} archived-file hashes and publication file checks')
