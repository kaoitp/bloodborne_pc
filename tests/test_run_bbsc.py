"""Observe the environment handed to the DLL launcher; no game process is started."""
from paths import ROOT
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('bbsc_run', ROOT / 'run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)


class BbscLaunchTests(unittest.TestCase):
    def launch_environment(self, extra):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory)
            (data / 'eboot.bin').touch()
            probe = data / 'launcher.exe'
            probe.touch()
            env = dict(BB_DATA_DIR=str(data), BB_GAME_DIR=str(data), BB_PROBE=str(probe),
                       BB_SKIP_GAME_CHECK='1', BB_FORCE_PATCHES='1', BB_RENDER_RES='1920x1080',
                       **extra)
            launched = []

            def child(command, **kwargs):
                if command[0] == str(probe):
                    launched.append(dict(os.environ))
                # The preparation programs are separate processes; their image work is
                # outside this launch-environment contract. mods.py returns the game path.
                return subprocess.CompletedProcess(command, 0, stdout=str(data), stderr='')

            previous = Path.cwd()
            try:
                with patch.dict(os.environ, env, clear=True), patch.object(sys, 'argv', ['run.py']), \
                     patch.object(subprocess, 'run', side_effect=child), patch.object(sys, 'path', sys.path.copy()):
                    self.assertEqual(run.main(), 0)
            finally:
                os.chdir(previous)
            self.assertEqual(len(launched), 1)
            return launched[0]

    def test_dll_guest_keeps_the_native_join_load(self):
        env = self.launch_environment({'BBSC_EMULATOR': 'test-emulator.exe'})
        self.assertEqual(env.get('SHADPS4_BBSC_WARP_JOIN'), '0')

    def test_explicit_reload_override_is_preserved(self):
        for value in ('0', '1'):
            with self.subTest(value=value):
                env = self.launch_environment({'BBSC_EMULATOR': 'test-emulator.exe',
                                               'SHADPS4_BBSC_WARP_JOIN': value})
                self.assertEqual(env['SHADPS4_BBSC_WARP_JOIN'], value)

    def test_empty_override_uses_the_single_load_default(self):
        env = self.launch_environment({'BBSC_EMULATOR': 'test-emulator.exe',
                                       'SHADPS4_BBSC_WARP_JOIN': ''})
        self.assertEqual(env['SHADPS4_BBSC_WARP_JOIN'], '0')

    def test_dll_receives_the_resolved_save_profile(self):
        env = self.launch_environment({'BBSC_EMULATOR': 'test-emulator.exe'})
        self.assertEqual(env.get('BB_USER_DIR'), str(Path(env['BB_DATA_DIR']) / 'user'))

    def test_stock_launch_does_not_change_bbsc_flags(self):
        env = self.launch_environment({})
        self.assertNotIn('SHADPS4_BBSC_WARP_JOIN', env)


if __name__ == '__main__':
    unittest.main()
