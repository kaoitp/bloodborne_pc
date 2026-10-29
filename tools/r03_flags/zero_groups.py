"""Which non-map flag groups are all zero in every world snapshot we have (1250-group JSON dumps)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
snaps = [p for p in (ROOT / '.superpowers').rglob('*.json')
         if p.stat().st_size > 100_000 and 'world' in p.name]
union = {}
count = 0
for path in snaps:
    try:
        groups = json.loads(path.read_text(encoding='utf-8')).get('groups')
    except Exception:
        continue
    if not isinstance(groups, dict) or len(groups) < 1000:
        continue
    count += 1
    for key, value in groups.items():
        raw = bytes.fromhex(value) if isinstance(value, str) else bytes(value)
        acc = union.setdefault(int(key), bytearray(len(raw)))
        for i, b in enumerate(raw):
            acc[i] |= b
print('snapshots', count, 'groups', len(union))
global_keys = [k for k in sorted(union) if not (1 <= k // 10000 <= 7 and 21 <= (k % 10000) // 100 <= 99)]
for k in global_keys:
    bits = sum(bin(b).count('1') for b in union[k])
    if '--all' in sys.argv or bits == 0:
        print(k, 'bits seen ON', bits)
