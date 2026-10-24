"""Build the pinned BBSC gameplay DLL using the existing Windows CLANG64 toolchain."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

PIN = '4f11faf88b6ba658ebde6fe5fbefdadedba4fa41'
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference', type=Path, help='existing pinned BBSC checkout')
    parser.add_argument('output', type=Path, help='local build directory (not release packaging)')
    args = parser.parse_args()
    reference, output = args.reference.resolve(), args.output.resolve()
    head = subprocess.check_output(['git', '-C', str(reference), 'rev-parse', 'HEAD'], text=True).strip()
    if head != PIN:
        parser.error('BBSC reference must be pinned at ' + PIN)
    compiler = shutil.which('clang++')
    if sys.platform != 'win32' or compiler is None:
        parser.error('run with the existing Windows CLANG64 clang++ on PATH')
    for patch in sorted((ROOT / 'gpu/patches/bbsc').glob('*.patch')):
        command = ['git', '-C', str(reference), 'apply']
        if subprocess.run(command + ['--reverse', '--check', str(patch)], capture_output=True).returncode:
            subprocess.run(command + ['--check', str(patch)], check=True)
            subprocess.run(command + [str(patch)], check=True)
    source = reference / 'emulator'
    for header in ('fmt/include/fmt/format.h', 'xbyak/xbyak/xbyak.h'):
        if not (source / 'externals' / header).is_file():
            parser.error('initialize the pinned fmt/xbyak submodules first')
    output.mkdir(parents=True, exist_ok=True)
    for name, source_name in (('LICENSE.txt', 'LICENSE'), ('NOTICE.txt', 'NOTICE.md'),
                              ('SUPPORTERS.txt', 'SUPPORTERS.txt')):
        notice = reference / source_name
        if not notice.is_file():
            parser.error('missing pinned mandatory notice: ' + source_name)
        shutil.copyfile(notice, output / name)
    files = [source / 'mod' / (name + '.cpp') for name in
             ('bbsc_mod', 'bbsc_hooks', 'bbsc_relay', 'bbsc_channel', 'bbsc_http', 'bbsc_discord')]
    files += [source / 'src/core' / name for name in ('bbsc_memscan.cpp', 'bloodborne_re.cpp')]
    command = [compiler, '-std=c++23', '-O2', '-g', '-fms-extensions', '-shared', '-static',
               '-DBBSC_MOD', '-DFMT_HEADER_ONLY', '-DNOMINMAX', '-DWIN32_LEAN_AND_MEAN',
               '-D_CRT_SECURE_NO_WARNINGS']
    for include in ('mod/shim', 'src', 'externals/fmt/include', 'externals/xbyak'):
        command.append('-I' + str(source / include))
    command.append('-I' + str(ROOT / 'gpu/bbnet'))
    command += [str(path) for path in files]
    command += ['-o', str(output / 'bbsc.dll'), '-lws2_32', '-lwinhttp', '-luser32']
    subprocess.run(command, check=True)
    print('bbsc.dll SHA256 ' + hashlib.sha256((output / 'bbsc.dll').read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
