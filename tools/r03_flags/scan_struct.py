"""Structured scan for references to candidate event-flag groups (R03 B18 save-flag research).

- emevd: every instruction argument, as aligned int32 (event/*.emevd.dcx, incl. sub-maps)
- esd: int32 literals (0x82 + int32) in every talk/chr ESD inside *.esdbnd.dcx
- params: every integer field of every param (paramdef layout), any width >= 2 bytes
- msb: aligned int32 (map/MapStudio)
- lua: float64 constants, any alignment (Lua 5.0 numbers are doubles)
- eboot.bin: int32 immediates, any alignment (code may also compute flags: not covered)
Usage: python -I scan_struct.py <dump>/dvdroot_ps4 <gamedata tools dir>
"""
import struct
import sys
from pathlib import Path

import numpy as np

DUMP = Path(sys.argv[1])
sys.path.insert(0, sys.argv[2])
import bbfiles  # noqa: E402
import emevd  # noqa: E402
import param  # noqa: E402

bbfiles.GAME = str(DUMP)
RANGES = {
    'group 8': (8000, 8999),
    'groups 10000-10009': (10_000_000, 10_009_999),
    'groups 60000-60009': (60_000_000, 60_009_999),
}
hits = {k: [] for k in RANGES}


def note(source, value):
    for label, (lo, hi) in RANGES.items():
        if lo <= value <= hi:
            hits[label].append((source, value))


def aligned_i32(source, data):
    n = len(data) // 4
    if n:
        ints = np.frombuffer(bytes(data[:4 * n]), dtype='<i4')
        for label, (lo, hi) in RANGES.items():
            for i in np.nonzero((ints >= lo) & (ints <= hi))[0]:
                hits[label].append((f'{source}+{4 * int(i):#x}', int(ints[i])))


# emevd
for path in sorted((DUMP / 'event').rglob('*.emevd.dcx')):
    ev = emevd.Emevd(str(path))
    for eid, instrs in ev.events:
        for bank, iid, args in instrs:
            aligned_i32(f'{path.name} ev{eid} {bank}[{iid}]', args)

# esd (0x82 int32 literals)
for path in sorted(DUMP.rglob('*esdbnd.dcx')):
    for name, (_, data) in bbfiles.read_bnd4(bbfiles.read_dcx(str(path))).items():
        i = data.find(b'\x82')
        while i != -1 and i + 5 <= len(data):
            note(f'{path.name}/{name}+{i:#x}', struct.unpack_from('<i', data, i + 1)[0])
            i = data.find(b'\x82', i + 1)

# params
defs = bbfiles.read_bnd4(bbfiles.read_dcx(str(DUMP / 'paramdef' / 'paramdef.paramdefbnd.dcx')))
params = bbfiles.read_bnd4(bbfiles.read_dcx(str(DUMP / 'param' / 'gameparam' / 'gameparam.parambnd.dcx')))
for pname, (_, pdata) in params.items():
    base = pname.rsplit('.', 1)[0]
    if base + '.paramdef' not in defs:
        print('no paramdef for', pname)
        continue
    lay, _ = param.layout(param.read_paramdef(defs[base + '.paramdef'][1]))
    for rid, off in param.read_param(pdata).items():
        for fname, value in param.row_values(lay, pdata, off).items():
            if isinstance(value, int):
                note(f'{base}[{rid}].{fname}', value)

# msb
for path in sorted((DUMP / 'map' / 'MapStudio').rglob('*.msb.dcx')):
    aligned_i32(path.name, bbfiles.read_dcx(str(path)))

# lua doubles
for path in sorted((DUMP / 'script').glob('*.luabnd.dcx')):
    for name, (_, data) in bbfiles.read_bnd4(bbfiles.read_dcx(str(path))).items():
        for a in range(8):
            n = (len(data) - a) // 8
            if n <= 0:
                continue
            d = np.frombuffer(data[a:a + 8 * n], dtype='<f8')
            with np.errstate(invalid='ignore'):
                for label, (lo, hi) in RANGES.items():
                    for i in np.nonzero((d >= lo) & (d <= hi) & (d == np.floor(d)))[0]:
                        hits[label].append((f'{path.name}/{name}+{a + 8 * int(i):#x} f64', float(d[i])))

# eboot immediates
eboot = (DUMP.parent / 'eboot.bin').read_bytes()
for a in range(4):
    n = (len(eboot) - a) // 4
    ints = np.frombuffer(eboot[a:a + 4 * n], dtype='<i4')
    for label, (lo, hi) in RANGES.items():
        for i in np.nonzero((ints >= lo) & (ints <= hi))[0]:
            hits[label].append((f'eboot+{a + 4 * int(i):#x}', int(ints[i])))

for label, found in hits.items():
    kinds = {}
    for src, _ in found:
        kind = 'eboot' if src.startswith('eboot') else src.split('.')[1] if '.' in src else src
        kinds[kind] = kinds.get(kind, 0) + 1
    print(f'{label}: {len(found)} hit(s) {kinds}')
    for h in found[:20]:
        print('   ', h)
