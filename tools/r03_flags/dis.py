"""Disassemble a function of the 01.09 eboot (fake SELF: text va 0 at file 0x28EB0 (SELF entry 1))."""
import sys

import capstone

EBOOT = sys.argv[3] if len(sys.argv) > 3 else "eboot.bin"  # the 01.09 dump eboot.bin

va = int(sys.argv[1], 0)
size = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x300
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
data = open(EBOOT, 'rb').read()
for ins in md.disasm(data[0x28EB0 + va:0x28EB0 + va + size], va):
    print(f'{ins.address:#010x}  {ins.mnemonic:8} {ins.op_str}')
    if ins.mnemonic == 'ret' and '--all' not in sys.argv:
        break
