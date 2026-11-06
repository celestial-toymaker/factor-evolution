"""核对公开汇总文件与候选计数。"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json

root = Path(__file__).resolve().parents[1]
read = lambda p: json.loads(p.read_text())
manifest = read(root / 'PUBLICATION_MANIFEST.json')
for item in manifest['files']:
    raw = (root / item['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['path']
rows = read(root / 'data/candidates.json')['candidates']
assert len(rows) == 56
assert set(Counter(r['family'] for r in rows).values()) == {8}
assert set(Counter((r['family'], r['round']) for r in rows).values()) == {4}
assert sum(r['nominated'] for r in rows) == 5
with (root / 'data/candidates.csv').open() as stream:
    csv_rows = list(csv.DictReader(stream))
assert len(csv_rows) == 56
for first, second in zip(rows, csv_rows):
    for key, value in first.items():
        assert str(value) == second[key], (first['trial_id'], key)
assert len(list((root / 'data/evaluation').glob('*.json'))) == 5
with (root / 'data/nominees.csv').open() as stream:
    assert len(list(csv.DictReader(stream))) == 15
print('校验通过：公开文件哈希、56 次候选、七路两轮、五个提名及阶段比较一致。')
