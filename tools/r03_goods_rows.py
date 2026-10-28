"""EquipParamGoods fields of the B15 boss reward goods, read from the user's own game dump.

Source only: it reads the two archives below from the dump folder given on the command line and prints
the rows; it writes nothing and no game data is kept in the repository. Used for
docs/handoff/R03-B15-EVIDENCE.md (dump APP_VER 01.09, CUSA03173).

    python tools/r03_goods_rows.py <dump>/dvdroot_ps4

Formats, as read here:
- DCX (DFLT): big-endian u32 size at 0x1C and compressed size at 0x20; zlib data 8 bytes after "DCA\\0".
- BND4: u32 file count at 0x0C, entry size (u64) at 0x20 must be 0x24; entries from 0x40:
  flags u32, -1 s32, compressed size u64, size u64, data offset u32, id s32, name offset u32.
  Byte 0x30 is 1 when names are UTF-16, 0 when Shift-JIS.
- PARAMDEF (paramdef.paramdefbnd.dcx, EquipParamGoods.paramdef): u16 field count at 0x08, u16 field
  size at 0x0A, fields from 0x38; per field the type name (fixstr) at +0x40 and the internal name at +0x90.
  A name "x:N" is an N-bit field; consecutive bit fields of one type share one unit, and dummy8 bit
  fields pack into u8 units; a field that does not fit starts the next unit.
- PARAM (gameparam.parambnd.dcx, EquipParamGoods.param): u16 row count at 0x0A; rows from 0x40, 0x18
  bytes each: row id u32, name offset u32, data offset u64.
The layout check: the computed row size must equal the spacing of the row data (108 bytes here).
"""
import argparse
import re
import struct
import sys
import zlib
from pathlib import Path

GAMEPARAM = 'param/gameparam/gameparam.parambnd.dcx'
PARAMDEF = 'paramdef/paramdef.paramdefbnd.dcx'
SIZES = {'s8': 1, 'u8': 1, 's16': 2, 'u16': 2, 's32': 4, 'u32': 4, 'f32': 4, 'dummy8': 1, 'fixstr': 1,
         'fixstrW': 2}
FORMATS = {'u8': '<B', 's8': '<b', 'u16': '<H', 's16': '<h', 'u32': '<I', 's32': '<i', 'f32': '<f'}
# goods id: (event, lot) of the B15 rows (BbscBossGoodsLots in bloodborne_re.cpp)
GOODS = {7150: (12201800, 21002950), 6109: (12301800, 80000000), 4001: (12401800, 50000001),
         4000: (12411800, 31000), 6539: (12421800, 80000300), 4323: (12601800, 55100000),
         7131: (12801800, 50700000), 1591: (13201800, 51001900), 6429: (13301800, 80000200),
         4020: (13501850, 3501850)}
SHOWN = ('goodsType', 'isConsume', 'isDrop', 'isDeposit', 'isOnlyOne', 'maxNum')


def dcx(data):
    if data[:4] != b'DCX\0' or data[0x28:0x2C] != b'DFLT':
        raise ValueError('not a DCX/DFLT file')
    size, compressed = struct.unpack_from('>II', data, 0x1C)
    start = data.index(b'DCA\0', 0x2C) + 8
    out = zlib.decompress(data[start:start + compressed])
    if len(out) != size:
        raise ValueError('DCX size mismatch')
    return out


def bnd4_name(data, at, wide):
    """The zero-terminated name at `at`; ValueError when it starts or runs past the end of the archive."""
    if at >= len(data):
        raise ValueError(f'BND4 name offset {at:#x} past the end ({len(data):#x})')
    if not wide:
        end = data.find(b'\0', at)
        if end < 0:
            raise ValueError(f'BND4 name at {at:#x} has no terminator')
        return data[at:end].decode('shift_jis', 'replace')
    for end in range(at, len(data) - 1, 2):
        if data[end:end + 2] == b'\0\0':
            return data[at:end].decode('utf-16le', 'replace')
    raise ValueError(f'BND4 name at {at:#x} has no terminator')


def bnd4_file(data, wanted):
    if len(data) < 0x40 or data[:4] != b'BND4' or struct.unpack_from('<Q', data, 0x20)[0] != 0x24:
        raise ValueError('unexpected BND4 layout')
    count = struct.unpack_from('<I', data, 0x0C)[0]
    if 0x40 + count * 0x24 > len(data):
        raise ValueError(f'BND4 entry table ({count} entries) runs past the end')
    for i in range(count):
        _, _, _, size, at, _, name_at = struct.unpack_from('<IiQQIiI', data, 0x40 + i * 0x24)
        name = bnd4_name(data, name_at, data[0x30] != 0)
        if name.replace('\\', '/').rsplit('/', 1)[-1] == wanted:
            if at + size > len(data):
                raise ValueError(f'{wanted} ({size} bytes at {at:#x}) runs past the end')
            return data[at:at + size]
    raise ValueError(f'{wanted} not in the archive')


def layout(paramdef):
    count, size = struct.unpack_from('<HH', paramdef, 0x08)
    fields, offset, bit, unit = {}, 0, 0, None
    for i in range(count):
        at = 0x38 + i * size
        kind = paramdef[at + 0x40:at + 0x48].split(b'\0')[0].decode()
        match = re.match(r'(\w+)(?:\[(\d+)\])?(?::\s*(\d+))?',
                         paramdef[at + 0x90:at + 0xB0].split(b'\0')[0].decode())
        name, length, bits = match.group(1), int(match.group(2) or 1), match.group(3)
        if bits is not None:
            kind = 'u8' if kind == 'dummy8' else kind
            if unit != kind or bit + int(bits) > SIZES[kind] * 8:
                offset += SIZES[unit] if unit else 0
                bit, unit = 0, kind
            fields[name] = (kind, offset, bit, int(bits))
            bit += int(bits)
            continue
        if unit:
            offset += SIZES[unit]
            bit, unit = 0, None
        fields[name] = (kind, offset, None, length)
        offset += SIZES[kind] * length
    return fields, offset + (SIZES[unit] if unit else 0)


def value(param, row_at, field):
    kind, offset, bit, n = field
    if bit is not None:
        unit = int.from_bytes(param[row_at + offset:row_at + offset + SIZES[kind]], 'little')
        return (unit >> bit) & ((1 << n) - 1)
    return struct.unpack_from(FORMATS[kind], param, row_at + offset)[0] if kind in FORMATS and n == 1 else None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dvdroot', type=Path, help='the dump folder holding param/ and paramdef/')
    args = parser.parse_args()
    fields, row_size = layout(bnd4_file(dcx((args.dvdroot / PARAMDEF).read_bytes()), 'EquipParamGoods.paramdef'))
    param = bnd4_file(dcx((args.dvdroot / GAMEPARAM).read_bytes()), 'EquipParamGoods.param')
    rows = {}
    for i in range(struct.unpack_from('<H', param, 0x0A)[0]):
        row_id, _, row_at = struct.unpack_from('<IIQ', param, 0x40 + i * 0x18)
        rows[row_id] = row_at
    starts = sorted(rows.values())
    spacing = starts[1] - starts[0]
    print(f'{len(fields)} fields, row size {row_size} from the layout, {spacing} from the data, {len(rows)} rows')
    if row_size != spacing:
        print('layout does not match the data')
        return 1
    print('field    ' + ' '.join(f'{name}@{fields[name][1]}' + (f'.{fields[name][2]}' if fields[name][2] is not None
                                                                   else '') for name in SHOWN))
    for goods, (event, lot) in GOODS.items():
        if goods not in rows:
            print(f'goods {goods} (event {event}, lot {lot}): not in the param')
            continue
        shown = ' '.join(f'{name}={value(param, rows[goods], fields[name])}' for name in SHOWN)
        print(f'goods {goods} (event {event}, lot {lot}): {shown}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
