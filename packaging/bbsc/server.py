#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Container startup, health checks and interactive shadNet account management."""
import argparse
import base64
import getpass
import ipaddress
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import subprocess
import sys
import urllib.request

DATA = Path("/data")
ASSETS = Path("/opt/shadnet")


def server_ip(variable="BBSC_SERVER_IP", default="127.0.0.1"):
    ip = ipaddress.IPv4Address(os.environ.get(variable) or default)
    if ip.is_unspecified or ip.is_multicast or ip == ipaddress.IPv4Address("255.255.255.255"):
        raise ValueError(f"{variable} must be a concrete LAN/Tailscale IPv4 address")
    return str(ip)


def drop_privileges():
    if os.geteuid() == 0:
        os.setgroups([])
        os.setgid(100)
        os.setuid(99)


def prepare_data():
    if os.geteuid() == 0:
        DATA.mkdir(parents=True, exist_ok=True)
        os.chown(DATA, 99, 100)
        # Migrate only the previous image's app user; leave Tailscale's root-owned state alone.
        for directory, dirs, files in os.walk(DATA):
            dirs[:] = [name for name in dirs if name != ".tailscale_state"]
            for name in dirs + files:
                path = Path(directory) / name
                if path.lstat().st_uid == 10001:
                    os.chown(path, 99, 100, follow_symlinks=False)


def initialize_shadnet(data, assets, ip):
    data.mkdir(parents=True, exist_ok=True)
    key_file = data / "registration-key"
    try:
        with open(key_file, "x", opener=lambda p, f: os.open(p, f, 0o600)) as out:
            out.write(secrets.token_hex(32) + "\n")
    except FileExistsError:
        pass
    key = key_file.read_text().strip()
    if not re.fullmatch(r"[0-9a-f]{64}", key):
        raise ValueError("Invalid /data/registration-key; restore its backup rather than replacing it")
    key_file.chmod(0o600)
    config = data / "shadnet.cfg"
    config.touch(mode=0o600, exist_ok=True)
    config.chmod(0o600)
    config.write_text(f"""[General]
Host={ip}
UnsecuredPort=31313
MatchingUdpPort=31314
WebApiPort=31315
Matching2Enabled=true
BloodborneSeamlessCoop=true
StatsEnabled=false
EmailValidated=false
RegistrationSecretKey={key}
""")
    # shadNet locates its database relative to the executable, regardless of WORKDIR.
    # copy2 would carry the image's SELinux label into a persistent volume.
    shutil.copy(assets / "shadnet", data / ".shadnet.next")
    (data / ".shadnet.next").replace(data / "shadnet")
    for name in ("worlds.cfg", "scoreboards.cfg"):
        if not (data / name).exists():
            shutil.copy(assets / name, data / name)


def account_succeeded(operation, returncode, output):
    # shortcut: this pinned sample exits zero on rejected replies; check its acknowledgement
    # until upstream supplies reliable exit codes.
    marker = "[create] Account created successfully." if operation == "register" else "[login] OK userId="
    return returncode == 0 and marker in output


def account(args, ip):
    password = getpass.getpass("Password: ") if sys.stdin.isatty() else sys.stdin.readline().rstrip("\r\n")
    if not password:
        raise ValueError("Password must not be empty")
    if args.command == "register" and sys.stdin.isatty() and getpass.getpass("Confirm password: ") != password:
        raise ValueError("Passwords do not match")
    command = [str(ASSETS / "shadnet-sample"), ip, "31313", args.command, args.username, "-"]
    key = ""
    if args.command == "register":
        command += [args.email, "-"]
        key = (DATA / "registration-key").read_text().strip()
    result = subprocess.run(command, input=password + "\n" + key + "\n",
                            env={**os.environ, "BBSC_ACCOUNT_STDIN": "1"},
                            capture_output=True, text=True, timeout=20)
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    return 0 if account_succeeded(args.command, result.returncode, result.stdout) else 1


def check_udp(ip, shadnet):
    transaction = secrets.token_bytes(16)
    request = (b"\xff" * 4 + b"\x01" + b"BBSCHealth".ljust(16, b"\0") + socket.inet_aton(ip)
               if shadnet else b"\x00\x01\x00\x00" + transaction)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(3)
        udp.connect((ip, 31314 if shadnet else 3478))
        udp.send(request)
        response = udp.recv(512)
    valid = (len(response) == 10 and response[:4] == b"\xff" * 4 if shadnet
             else len(response) >= 20 and response[:2] == b"\x01\x01" and response[4:20] == transaction)
    if not valid:
        raise ValueError("UDP STUN health check failed")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("shadnet", "gameserver", "health-shadnet", "health-gameserver", "register", "login"))
    parser.add_argument("username", nargs="?")
    parser.add_argument("email", nargs="?")
    args = parser.parse_args(argv)
    ip = server_ip()
    shadnet_ip = server_ip("BBSC_SHADNET_IP", ip) if args.command == "gameserver" else ip
    if args.command in ("shadnet", "gameserver"):
        prepare_data()
    drop_privileges()
    if args.command == "shadnet":
        initialize_shadnet(DATA, ASSETS, ip)
        os.execv(str(DATA / "shadnet"), [str(DATA / "shadnet")])
    elif args.command == "gameserver":
        os.execvp("python3", ["python3", "-u", "/opt/bbsc-gameserver/bbsc_gameserver.py",
                             "--host", ip, "--shadnet", shadnet_ip,
                             "--bbhost-public-ip", ip, "--bbhost-port", "0",
                             "--bbhost-stun-port", "3478", "--relay-port", "0", "--no-playlog",
                             "--data", "/data/online-data.json", "--log-dir", "/data/logs"])
    elif args.command.startswith("health-"):
        shadnet = args.command == "health-shadnet"
        path = "31315/status" if shadnet else "20443/bb-eu/ss.info"
        # Private addresses must not be sent through an HTTP proxy inherited by the container.
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(f"http://{ip}:{path}", timeout=3) as response:
            body = response.read()
        if shadnet:
            if json.loads(body).get("ok") is not True:
                raise ValueError("WebAPI health check failed")
            with socket.create_connection((ip, 31313), timeout=3):
                pass
        else:
            if b"<gameurl2>" not in base64.b64decode(body, validate=True):
                raise ValueError("Game server health check failed")
        check_udp(ip, shadnet)
    else:
        if not args.username or (args.command == "register" and not args.email):
            parser.error("register requires USERNAME EMAIL; login requires USERNAME")
        return account(args, ip)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.TimeoutExpired:
        sys.exit("Account request timed out")
    except (OSError, ValueError, AssertionError) as error:
        sys.exit(str(error) or "Health check failed")
