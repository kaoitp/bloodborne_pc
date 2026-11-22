"""Prepare the pinned Seamless engine and package a local Windows BBSC preview."""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from fetch_yharnam import download, sha256
from package_files import check, write


PORT_VERSION = '1.9.8.6'
PREVIEW_VERSION = '1.5.0'
ENGINE = 'bb-probe-seamless.exe'
PORT_RELEASE = f'https://github.com/Supermedo/bloodborne_pc/releases/download/windows-v{PORT_VERSION}'
BBSC_RELEASE = ('https://github.com/Amanises-Yharnam-Together/BBSC-Yharnam-Together/releases/download/'
                f'v{PREVIEW_VERSION}')
ENGINE_SOURCE = (PORT_RELEASE, f'bb-probe-seamless-{PORT_VERSION}-source.zip',
                 '2fc82471bc71965ede76cbcab3c19ea03854014340f1704252ee750b6ba4d8ef')
WINDOWS_PACKAGE = (PORT_RELEASE, 'Bloodborne-Windows.zip',
                   '182be6863141c9c7e4622731e67a2c25ee3dfe97f62255bfb2af1a194c673317')
BBSC_PACKAGE = (BBSC_RELEASE, f'YharnamTogether-v{PREVIEW_VERSION}-portable.zip',
                '2aaa8e4cd39c25c56dbf6add967b8875fbe004e515622e52b9bb2ce80ae3e38e')
BBSC_FILES = ('tools/party_boss_events.py', 'scripts/hud_patch.py', 'scripts/party_hud_icons.bin',
              'event-reference.json', 'LICENSE', 'CREDITS.txt', 'VERSION.txt')
PATCH = ROOT / 'packaging/bbsc/bbsc-1.5.0-bbport.patch'
PREVIEW_README = Path(__file__).with_name('BBSC-1.5.0-PREVIEW.txt')


def archive(cache, source):
    release, name, expected = source
    file = Path(cache) / name
    if not file.is_file():
        download(file, f'{release}/{name}')
    if sha256(file) != expected:
        raise ValueError(f'Unexpected SHA-256 for {file}')
    return ZipFile(file)


def prepare(cache, dest):
    """Apply the port to a fresh copy of the published 1.9.8.6 Seamless source."""
    if dest.exists():
        raise FileExistsError(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=dest.parent) as work:
        with archive(cache, ENGINE_SOURCE) as upstream:
            upstream.extractall(work)
        source = Path(work) / 'bb-probe-seamless-src'
        env = {**os.environ, 'GIT_CEILING_DIRECTORIES': str(Path(work).resolve())}
        subprocess.run(['git', '-c', 'core.autocrlf=false', 'apply', str(PATCH)], cwd=source, env=env, check=True)
        source.rename(dest)
    print(dest)


def copy_runtime(engine, stock, dest, clang):
    """Keep the new executable and its own transitive DLL dependencies in one directory."""
    dest.mkdir()
    subprocess.run([str(clang / 'llvm-strip.exe'), '--strip-debug', '-o', str(dest / ENGINE), str(engine)], check=True)
    # These upscaling and frame-generation DLLs are loaded explicitly at run time.
    extras = [p for p in stock.glob('*.dll') if p.name.lower().startswith(
        ('amd_fidelityfx_', 'bbport_dlss', 'd3d12core', 'd3d12sdklayers', 'libxess', 'nvngx', 'xess'))]
    for file in extras:
        shutil.copy2(file, dest)
    for folder in ('fsr24', 'LocalChalice'):
        if (stock / folder).is_dir():
            shutil.copytree(stock / folder, dest / folder)

    system = Path(os.environ['SystemRoot']) / 'System32'
    visited = set()
    pending = [dest / ENGINE, *dest.glob('*.dll'), *dest.glob('fsr24/*.dll')]
    while pending:
        binary = pending.pop()
        if binary in visited:
            continue
        visited.add(binary)
        result = subprocess.check_output([str(clang / 'llvm-readobj.exe'), '--coff-imports', str(binary)], text=True)
        for name in re.findall(r'^\s+Name: (\S+\.dll)\s*$', result, re.M | re.I):
            if name.lower().startswith(('api-ms-', 'ext-ms-')) or name.lower() == 'vulkan-1.dll':
                continue
            dll = dest / name
            if not dll.is_file():
                source = clang / name
                if not source.is_file():
                    source = stock / name
                if source.is_file():
                    shutil.copy2(source, dll)
                elif (system / name).is_file():
                    continue
                else:
                    raise FileNotFoundError(f'{binary.name} needs {name}')
            pending.append(dll)


def package(cache, engine, launcher, output, clang):
    """Make a clean portable test ZIP from the official BBport package and the rebuilt runtime."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as work:
        work = Path(work)
        with archive(cache, WINDOWS_PACKAGE) as upstream:
            upstream.extractall(work)
        port = work / 'bbport-windows'
        shutil.copy2(launcher / 'Bloodborne.exe', port)
        shutil.rmtree(port / '_internal')
        shutil.copytree(launcher / '_internal', port / '_internal')
        (port / 'bin' / ENGINE).unlink()
        copy_runtime(engine, port / 'bin', port / 'bin' / f'bbsc-{PREVIEW_VERSION}', clang)
        with archive(cache, BBSC_PACKAGE) as bbsc:
            for name in BBSC_FILES:
                (port / 'seamless' / name).write_bytes(bbsc.read(f'Yharnam Together/{name}'))
        (port / 'seamless' / 'bbport-seamless.txt').write_text(
            f'BBSC: Yharnam Together {PREVIEW_VERSION} on SuperMedo BBport {PORT_VERSION}\n'
            f'BBSC files: {BBSC_PACKAGE[0]}/{BBSC_PACKAGE[1]}\n'
            f'BBport engine base: {ENGINE_SOURCE[0]}/{ENGINE_SOURCE[1]}\n'
            f'Engine adaptations: {PATCH.name}\n',
            encoding='utf-8')
        shutil.copy2(PATCH, port / 'seamless')
        shutil.copy2(PREVIEW_README, port)
        # Match the normal run.py integrity check and include the isolated Seamless runtime.
        write(port, PORT_VERSION)
        if check(port) != (PORT_VERSION, []):
            raise RuntimeError('Program file integrity check failed')
        windows = Path(os.environ['SystemRoot'])
        env = {**os.environ, 'PATH': os.pathsep.join((str(windows / 'System32'), str(windows)))}
        binary = port / 'bin' / f'bbsc-{PREVIEW_VERSION}' / ENGINE
        result = subprocess.run([str(binary)], cwd=port, env=env, capture_output=True, text=True, timeout=20)
        if 'Usage:' not in result.stderr:
            raise RuntimeError(f'Seamless executable did not reach main: {result.returncode} {result.stderr}')
        stage = work / output.stem
        port.rename(stage)
        packed = Path(shutil.make_archive(str(work / 'package'), 'zip', work, stage.name))
        with ZipFile(packed) as result:
            if bad := result.testzip():
                raise RuntimeError(f'Failed ZIP integrity check: {bad}')
        packed.replace(output)
    output.with_suffix('.zip.sha256').write_text(f'{sha256(output)}  {output.name}\n', encoding='ascii')
    print(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    setup = sub.add_parser('prepare')
    setup.add_argument('cache', type=Path)
    setup.add_argument('dest', type=Path)
    stage = sub.add_parser('package')
    stage.add_argument('cache', type=Path)
    stage.add_argument('engine', type=Path)
    stage.add_argument('launcher', type=Path)
    stage.add_argument('output', type=Path)
    stage.add_argument('--clang', type=Path, default=Path('C:/msys64/clang64/bin'))
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args.cache.resolve(), args.dest.resolve())
    else:
        package(args.cache.resolve(), args.engine.resolve(), args.launcher.resolve(), args.output.resolve(),
                args.clang.resolve())


if __name__ == '__main__':
    main()
