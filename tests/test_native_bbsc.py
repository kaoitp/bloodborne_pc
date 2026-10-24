"""Exercise production shader and native BBSC recovery boundaries without game assets."""
from paths import ROOT
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


@unittest.skipUnless(shutil.which('clang++'), 'clang++ and the GPU build headers are required')
class NativeBoundaryTests(unittest.TestCase):
    def run_fixture(self, name):
        compiler = shutil.which('clang++')
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / ('native-boundary.exe' if os.name == 'nt' else 'native-boundary')
            command = [compiler, '-std=c++23', '-O0']
            for include in ('gpu/shim', 'gpu/shadps4', 'gpu/bbnet', 'gpu/third_party/magic_enum/include'):
                command.append('-I' + str(ROOT / include))
            subprocess.run(command + [str(ROOT / 'tests/native' / name), '-o', str(binary)],
                           check=True, text=True)
            subprocess.run([str(binary)], check=True, text=True)

    def test_absent_tables_and_existing_reads(self):
        self.run_fixture('shader_user_data.cpp')

    def test_durable_return_record(self):
        self.run_fixture('bbsc_home_spot.cpp')


if __name__ == '__main__':
    unittest.main()
