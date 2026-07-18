#!/usr/bin/env python3
import hashlib, json, re
from pathlib import Path
from urllib.parse import urlsplit
root=Path(__file__).resolve().parents[1]
assert (root/'website/index.html').exists()
assert (root/'distribution/components').exists()
assert sum(1 for _ in (root/'distribution/components').glob('*/component.json')) == 24
manifest=json.loads((root/'DISTRIBUTION_MANIFEST.json').read_text())
for row in manifest['files']:
    p=root/row['path']; assert p.exists(), row['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'], row['path']
missing=[]
for page in (root/'website').rglob('*.html'):
    text=page.read_text(encoding='utf-8',errors='replace')
    for target in re.findall(r'(?i)(?:href|src)=["\']([^"\']+)["\']', text):
        if target.startswith(('#','http:','https:','mailto:','tel:','data:','javascript:')): continue
        path=urlsplit(target).path
        if not path: continue
        dest=(page.parent/path).resolve()
        if path.endswith('/') or dest.is_dir(): dest=dest/'index.html'
        if not dest.exists(): missing.append((str(page.relative_to(root)),target))
assert not missing, missing[:20]
print(json.dumps({'status':'PASS','components':24,'website_pages':sum(1 for _ in (root/'website').rglob('*.html'))},indent=2))
