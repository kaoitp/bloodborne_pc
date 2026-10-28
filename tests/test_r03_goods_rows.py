"""The BND4 reader of tools/r03_goods_rows.py on small synthetic archives: valid names and members parse,
malformed input is rejected and never hangs (PR #16 review 2). No game data."""
from paths import ROOT
import importlib.util
import struct
import unittest

spec = importlib.util.spec_from_file_location('r03_goods_rows', ROOT / 'tools/r03_goods_rows.py')
goods_rows = importlib.util.module_from_spec(spec)
spec.loader.exec_module(goods_rows)


def bnd4(files, wide=True):
    """A BND4 with one entry per (name, content), names and data after the entry table."""
    head = 0x40 + len(files) * 0x24
    names = b''.join((n.encode('utf-16le') + b'\0\0') if wide else (n.encode() + b'\0') for n, _ in files)
    out = bytearray(head) + names
    out += b'\0' * (-len(out) % 16)
    name_at = head
    for i, (name, content) in enumerate(files):
        struct.pack_into('<IiQQIiI', out, 0x40 + i * 0x24, 0x40, -1, len(content), len(content), len(out), i,
                         name_at)
        name_at += len(name.encode('utf-16le') if wide else name.encode()) + (2 if wide else 1)
        out += content
    out[:4] = b'BND4'
    struct.pack_into('<I', out, 0x0C, len(files))
    struct.pack_into('<Q', out, 0x20, 0x24)
    out[0x30] = 1 if wide else 0
    return out


class GoodsRowsBnd4Tests(unittest.TestCase):
    def test_valid_members(self):
        for wide in (True, False):
            data = bnd4([('N:\\x\\A.param', b'aaaa'), ('N:\\x\\EquipParamGoods.param', b'goods')], wide)
            self.assertEqual(goods_rows.bnd4_file(bytes(data), 'EquipParamGoods.param'), b'goods')
            with self.assertRaises(ValueError):
                goods_rows.bnd4_file(bytes(data), 'Missing.param')

    def test_name_offset_at_the_end(self):
        # the review's case: 100 bytes, one entry, name offset 100, UTF-16 names - used to loop forever
        data = bytearray(100)
        data[:4] = b'BND4'
        struct.pack_into('<I', data, 0x0C, 1)
        struct.pack_into('<Q', data, 0x20, 0x24)
        data[0x30] = 1
        struct.pack_into('<IiQQIiI', data, 0x40, 0x40, -1, 0, 0, 0, 0, 100)
        for wide in (1, 0):
            data[0x30] = wide
            with self.assertRaises(ValueError):
                goods_rows.bnd4_file(bytes(data), 'EquipParamGoods.param')

    def test_name_without_terminator(self):
        for wide in (True, False):
            data = bnd4([('EquipParamGoods.param', b'goods')], wide)
            name_at = struct.unpack_from('<I', data, 0x40 + 0x20)[0]
            cut = bytes(data[:name_at + 6])   # the name runs into the end of the file
            with self.assertRaises(ValueError):
                goods_rows.bnd4_file(cut, 'EquipParamGoods.param')

    def test_member_past_the_end(self):
        data = bnd4([('EquipParamGoods.param', b'goods')])
        with self.assertRaises(ValueError):
            goods_rows.bnd4_file(bytes(data[:-2]), 'EquipParamGoods.param')

    def test_short_or_truncated_table(self):
        with self.assertRaises(ValueError):
            goods_rows.bnd4_file(b'BND4', 'EquipParamGoods.param')
        data = bnd4([('A', b'a'), ('B', b'b')])
        struct.pack_into('<I', data, 0x0C, 1000)
        with self.assertRaises(ValueError):
            goods_rows.bnd4_file(bytes(data), 'B')


if __name__ == '__main__':
    unittest.main()
