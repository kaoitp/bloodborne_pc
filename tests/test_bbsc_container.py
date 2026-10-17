import importlib.util
import io
import base64
import http.client
import os
from pathlib import Path
import tempfile
import socket
import subprocess
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch


ENTRY = Path(__file__).resolve().parents[1] / "packaging/bbsc/server.py"
spec = importlib.util.spec_from_file_location("bbsc_container", ENTRY)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class BbscContainerTests(unittest.TestCase):
    def test_migration_keeps_tailscale_state_private_and_does_not_follow_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            data.mkdir()
            (data / "registration-key").write_text("old key")
            (data / ".tailscale_state").mkdir()
            (data / ".tailscale_state/tailscaled.state").write_text("private")
            outside = Path(tmp) / "outside"
            outside.write_text("untouched")
            (data / "link").symlink_to(outside)
            with patch.object(server, "DATA", data), patch.object(server.os, "geteuid", return_value=0), \
                    patch.object(Path, "lstat", return_value=SimpleNamespace(st_uid=10001)), \
                    patch.object(server.os, "chown") as chown:
                server.prepare_data()
            self.assertEqual(chown.call_count, 3)
            chown.assert_any_call(data, 99, 100)
            chown.assert_any_call(data / "registration-key", 99, 100, follow_symlinks=False)
            chown.assert_any_call(data / "link", 99, 100, follow_symlinks=False)

    def test_root_hook_hands_off_to_unprivileged_server(self):
        calls = []
        with patch.object(server.os, "geteuid", return_value=0), \
                patch.object(server.os, "setgroups", side_effect=lambda x: calls.append(("groups", x))), \
                patch.object(server.os, "setgid", side_effect=lambda x: calls.append(("gid", x))), \
                patch.object(server.os, "setuid", side_effect=lambda x: calls.append(("uid", x))):
            server.drop_privileges()
        self.assertEqual(calls, [("groups", []), ("gid", 100), ("uid", 99)])
        with patch.object(server.os, "geteuid", return_value=99), \
                patch.object(server.os, "setuid") as setuid:
            server.drop_privileges()
        setuid.assert_not_called()

    def test_game_server_defaults_to_its_own_shadnet_address(self):
        with patch.dict(os.environ, {"BBSC_SERVER_IP": "127.0.0.2", "BBSC_SHADNET_IP": ""}), \
                patch.object(server.os, "execvp") as execute:
            server.main(["gameserver"])
        command = execute.call_args.args[1]
        self.assertEqual(command[command.index("--shadnet") + 1], "127.0.0.2")

    def test_game_server_rejects_invalid_shadnet_address(self):
        for value in ("0.0.0.0", "224.0.0.1", "bad\nHost=0.0.0.0"):
            with self.subTest(value=value), \
                    patch.dict(os.environ, BBSC_SHADNET_IP=value), \
                    patch.object(server.os, "execvp") as execute:
                with self.assertRaises(ValueError):
                    server.main(["gameserver"])
                execute.assert_not_called()

    def test_only_concrete_ipv4_addresses_are_advertised(self):
        for value in ("0.0.0.0", "::1", "224.0.0.1", "host\nStatsEnabled=true"):
            with self.subTest(value=value), patch.dict(os.environ, BBSC_SERVER_IP=value):
                with self.assertRaises(ValueError):
                    server.server_ip()
        with patch.dict(os.environ, BBSC_SERVER_IP="100.101.102.103"):
            self.assertEqual(server.server_ip(), "100.101.102.103")

    def test_restart_keeps_accounts_and_signup_key_but_updates_binary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets, data = root / "assets", root / "data"
            assets.mkdir()
            data.mkdir()
            for name in ("shadnet", "worlds.cfg", "scoreboards.cfg"):
                (assets / name).write_text("version one")
            server.initialize_shadnet(data, assets, "127.0.0.1")
            key = (data / "registration-key").read_text()
            self.assertEqual(len(key.strip()), 64)
            self.assertEqual((data / "registration-key").stat().st_mode & 0o777, 0o600)
            (data / "db").mkdir()
            (data / "db/shadnet.db").write_bytes(b"existing accounts")
            (assets / "shadnet").write_text("version two")
            server.initialize_shadnet(data, assets, "100.101.102.103")
            self.assertEqual((data / "registration-key").read_text(), key)
            self.assertEqual((data / "db/shadnet.db").read_bytes(), b"existing accounts")
            self.assertEqual((data / "shadnet").read_text(), "version two")
            config = (data / "shadnet.cfg").read_text()
            self.assertIn("Host=100.101.102.103\n", config)
            self.assertIn("BloodborneSeamlessCoop=true\n", config)
            self.assertIn("RegistrationSecretKey=" + key.strip(), config)
            self.assertNotIn("StatsEnabled=true", config)

    def test_invalid_existing_key_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "registration-key").write_text("broken\nHost=0.0.0.0")
            with self.assertRaises(ValueError):
                server.initialize_shadnet(data, data, "127.0.0.1")
            self.assertEqual((data / "registration-key").read_text(), "broken\nHost=0.0.0.0")

    def test_image_xattrs_do_not_leak_into_persistent_volume(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets, data = root / "assets", root / "data"
            assets.mkdir()
            for name in ("shadnet", "worlds.cfg", "scoreboards.cfg"):
                (assets / name).write_text("image file")
                try:
                    os.setxattr(assets / name, "user.bbsc-image-label", b"old-container-label")
                except (OSError, AttributeError):
                    self.skipTest("File-system extended attributes unavailable")
            server.initialize_shadnet(data, assets, "127.0.0.1")
            for name in ("shadnet", "worlds.cfg", "scoreboards.cfg"):
                self.assertNotIn("user.bbsc-image-label", os.listxattr(data / name))

    def test_sample_tool_rejected_reply_is_not_reported_as_success(self):
        self.assertFalse(server.account_succeeded("register", 0, "[create] FAILED: ExistingUsername"))
        self.assertFalse(server.account_succeeded("login", 0, "[login] FAILED: LoginError"))
        self.assertFalse(server.account_succeeded("register", 1, "[create] Account created successfully."))
        self.assertTrue(server.account_succeeded("register", 0, "[create] Account created successfully."))
        self.assertTrue(server.account_succeeded("login", 0, "[login] OK userId=1"))

    def test_udp_health_requires_reply_from_both_protocols(self):
        transaction = b"t" * 16
        for shadnet, reply in ((True, b"\xff" * 4 + b"\x7f\0\0\x01\x12\x34"),
                               (False, b"\x01\x01\0\0" + transaction)):
            with self.subTest(shadnet=shadnet), patch.object(server.socket, "socket") as sock, \
                    patch.object(server.secrets, "token_bytes", return_value=transaction):
                udp = sock.return_value.__enter__.return_value
                udp.recv.return_value = reply
                server.check_udp("127.0.0.1", shadnet)
                udp.connect.assert_called_with(("127.0.0.1", 31314 if shadnet else 3478))
                udp.recv.return_value = b"bad reply"
                with self.assertRaises(ValueError):
                    server.check_udp("127.0.0.1", shadnet)

    def test_account_secrets_do_not_appear_in_child_arguments(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            key = "a" * 64
            (data / "registration-key").write_text(key)
            args = SimpleNamespace(command="register", username="HunterOne", email="hunter1@example.test")
            with patch.object(server, "DATA", data), patch.object(server.sys, "stdin", io.StringIO("private-password\n")), \
                    patch.object(server.sys, "stdout", io.StringIO()), patch.object(server.subprocess, "run") as run:
                run.return_value = SimpleNamespace(returncode=0, stdout="[create] Account created successfully.", stderr="")
                self.assertEqual(server.account(args, "127.0.0.1"), 0)
                command = run.call_args.args[0]
                self.assertNotIn("private-password", command)
                self.assertNotIn(key, command)
                self.assertEqual(run.call_args.kwargs["input"], "private-password\n" + key + "\n")
                self.assertEqual(run.call_args.kwargs["env"]["BBSC_ACCOUNT_STDIN"], "1")

    def test_same_pc_server_list_uses_the_address_that_is_listening(self):
        ip = "127.0.0.2"  # Emulate a host connecting from its own LAN/Tailscale address.
        shadnet_ip = "127.0.0.3"
        with patch.dict(os.environ, BBSC_SERVER_IP=ip, BBSC_SHADNET_IP=shadnet_ip), \
                patch.object(server.os, "execvp") as execute:
            server.main(["gameserver"])
        command = execute.call_args.args[1]
        command[2] = str(ENTRY.parents[2] / "scripts/bbsc_gameserver/bbsc_gameserver.py")
        try:
            with socket.socket() as reserve:
                reserve.bind((ip, 0))
                port = reserve.getsockname()[1]
        except PermissionError:
            self.skipTest("Loopback sockets are blocked in this sandbox")
        with tempfile.TemporaryDirectory() as tmp:
            command += ["--port", str(port)]
            for flag, value in (("--bbhost-stun-port", "0"), ("--data", tmp + "/data.json"),
                                ("--log-dir", tmp + "/logs")):
                command[command.index(flag) + 1] = value
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            try:
                for _ in range(60):
                    connection = http.client.HTTPConnection(ip, port, timeout=1, source_address=(ip, 0))
                    try:
                        connection.request("GET", "/bb-eu/ss.info")
                        response = connection.getresponse()
                        xml = base64.b64decode(response.read()).decode()
                        break
                    except OSError:
                        time.sleep(0.05)
                    finally:
                        connection.close()
                else:
                    self.fail("Game server did not become ready")
                self.assertIn(f"<api_Login>http://{ip}:{port}</api_Login>", xml)
                self.assertNotIn("http://127.0.0.1:20443", xml)
                for action in ("Create", "GetList", "Remove", "Summon"):
                    self.assertIn(f"<api_SummonData{action}>http://{shadnet_ip}:31315</api_SummonData{action}>", xml)
                self.assertNotIn(f"http://{ip}:31315", xml)
            finally:
                process.terminate()
                process.communicate(timeout=5)


if __name__ == "__main__":
    unittest.main()
