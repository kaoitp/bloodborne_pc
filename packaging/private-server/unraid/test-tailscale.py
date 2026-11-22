"""Exercise the official Unraid hook on a disposable Headscale network."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid

HEADSCALE = 'ghcr.io/juanfont/headscale:v0.29.7'
HOOK = ('https://raw.githubusercontent.com/unraid/webgui/6ed056248a1ffa5d99f1bf4339aab43d50bddd68'
        '/share/docker/tailscale_container_hook')
CONFIG = '''server_url: http://control:8080
listen_addr: 0.0.0.0:8080
noise:
  private_key_path: /var/lib/headscale/noise_private.key
prefixes:
  v4: 100.64.0.0/24
derp:
  urls:
    - https://controlplane.tailscale.com/derpmap/default
database:
  type: sqlite
  sqlite:
    path: /var/lib/headscale/db.sqlite
dns:
  magic_dns: false
  override_local_dns: false
logtail:
  enabled: false
'''


def docker(*args, env=None):
    return subprocess.run(['docker', *args], check=True, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=45,
                          env=None if env is None else os.environ | env).stdout.strip()


def wait_for(check, description):
    for _ in range(30):
        try:
            return check()
        except (AssertionError, subprocess.CalledProcessError):
            time.sleep(1)
    raise RuntimeError(f'Timed out waiting for {description}')


def udp_packets(container):
    rows = docker('exec', container, 'cat', '/proc/net/snmp').splitlines()
    names, counts = [row.split() for row in rows if row.startswith('Udp:')]
    return int(counts[names.index('InDatagrams')])


def verify(image, folder):
    prefix = 'bbsc-unraid-test-' + uuid.uuid4().hex[:8]
    network, control, host, peer = (prefix + '-' + role for role in ('net', 'control', 'host', 'peer'))
    hook = folder / 'tailscale_container_hook'
    with urllib.request.urlopen(HOOK, timeout=20) as response:
        hook.write_bytes(response.read())
    config = folder / 'config.yaml'
    config.write_text(CONFIG, encoding='utf-8')
    entrypoint = ' '.join(json.loads(docker('image', 'inspect', '--format', '{{json .Config.Entrypoint}}', image)))
    docker('network', 'create', network)
    try:
        docker('run', '-d', '--name', control, '--network', network, '--network-alias', 'control',
               '--mount', f'type=bind,src={config},dst=/etc/headscale/config.yaml,readonly', HEADSCALE, 'serve')
        wait_for(lambda: docker('exec', control, 'headscale', 'health'), 'Headscale')
        user = json.loads(docker('exec', control, 'headscale', 'users', 'create', 'smoke', '--output', 'json'))

        for container, original_entrypoint in ((host, entrypoint), (peer, '/bin/sleep infinity')):
            key = docker('exec', control, 'headscale', 'preauthkeys', 'create', '--user', str(user['id']),
                         '--expiration', '10m')
            docker('create', '--name', container, '--network', network, '--cap-add', 'NET_ADMIN',
                   '--device', '/dev/net/tun', '--entrypoint', '/bin/sh',
                   '-e', 'TAILSCALE_USERSPACE_NETWORKING=false', '-e', 'TAILSCALE_STATE_DIR=/data/.tailscale_state',
                   '-e', f'TAILSCALE_HOSTNAME={container}', '-e', f'ORG_ENTRYPOINT={original_entrypoint}',
                   '-e', 'TAILSCALE_PARAMS', image, '/unraid-hook.sh',
                   env={'TAILSCALE_PARAMS': f'--login-server=http://control:8080 --auth-key={key} --accept-dns=false'})
            docker('cp', str(hook), f'{container}:/unraid-hook.sh')
            docker('start', container)

        wait_for(lambda: docker('exec', host, 'curl', '-fsS', 'http://127.0.0.1:20443/status'), 'the game server')
        address = docker('exec', host, 'tailscale', 'ip', '-4')
        assert address.startswith('100.64.0.')
        for port in (31315, 20443):
            wait_for(lambda: docker('exec', peer, 'curl', '-fsS', '--max-time', '2', f'http://{address}:{port}/status'),
                     f'Tailnet TCP port {port}')

        before = udp_packets(host)
        docker('exec', peer, '/bin/bash', '-c',
               'exec 3>/dev/udp/"$1"/31314; for n in {1..16}; do printf probe >&3; done', 'udp-test', address)
        wait_for(lambda: assert_udp(host, before), 'Tailnet UDP port 31314')

        processes = docker('exec', host, 'sh', '-c', "awk '/^Name:/ { name=$2 } /^Uid:/ { print name, $3 }' "
                           '/proc/[0-9]*/status 2>/dev/null || true').splitlines()
        assert 'shadnet 10001' in processes
        assert 'tailscaled 0' in processes
        assert not json.loads(docker('inspect', host, '--format', '{{json .HostConfig.PortBindings}}'))
        docker('exec', host, 'sh', '-c', 'test -s /data/link_key.bin && test -s /data/.tailscale_state/tailscaled.state')
        print('Official Unraid hook passed. Tailnet UDP 31314 and both TCP ports are reachable, and shadNet runs as UID 10001.')
    finally:
        for container in (host, peer, control):
            subprocess.run(['docker', 'rm', '-f', '-v', container], capture_output=True, timeout=15)
        subprocess.run(['docker', 'network', 'rm', network], capture_output=True, timeout=15)


def assert_udp(host, before):
    assert udp_packets(host) >= before + 16


if __name__ == '__main__':
    try:
        with tempfile.TemporaryDirectory() as scratch:
            verify(sys.argv[1], Path(scratch).resolve())
    except subprocess.CalledProcessError as error:
        print(re.sub(r'hskey-[\w-]+', '[redacted]', error.stderr or ''), file=sys.stderr)
        raise
