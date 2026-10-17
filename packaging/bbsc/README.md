# BBSC server containers (Linux)

Two containers for the BBSC client in this port: shadNet accounts/matchmaking/WebAPI, and the
bundled Python game server with the BBSC UDP relay. No game files or GPU are needed on the server.
The server can be the same Linux PC used to play.

For Unraid's per-container Tailscale startup hook and separate IPs, see [Unraid setup](UNRAID.th.md).

Use a trusted LAN or Tailscale network: shadNet's TCP protocol is unencrypted. Every player must
be able to reach the server and the other players. These containers use Linux host networking
to preserve the source IP/port needed by STUN and P2P; Docker Desktop networking is not tested.

## Start

Install Docker Engine with Compose, or Podman with `podman-compose`. In the commands below,
replace `docker compose` with `podman-compose` when using Podman.

If you downloaded the prebuilt server archive, extract it and load its images first:

```sh
tar -xzf BBSC-Server-Linux-x86_64-unraid-tailscale.tar.gz
cd bbsc-server
docker load -i images.tar
cd packaging/bbsc
cp .env.example .env
```

With Podman, load with `podman load -i images.tar`. Edit `.env` so `BBSC_SERVER_IP` is this
machine's LAN or Tailscale IPv4 address (for example `100.101.102.103`). The default
`127.0.0.1` is for local testing only. It must be an address assigned to the server; do not use
`0.0.0.0`, a container IP, or another player's address.

```sh
docker compose up -d --no-build
docker compose ps
docker compose logs --tail 30
```

Wait for both services to show `healthy` before creating accounts.

When building from this repository instead, run from `packaging/bbsc`:

```sh
cp .env.example .env
# Edit BBSC_SERVER_IP in .env before starting.
docker compose build
docker compose up -d --no-build
```

This PC's builds are run from `distrobox enter bbport-dev`, forwarding Podman commands to the
host with `distrobox-host-exec podman`. The Dockerfile builds shadNet itself in an isolated build
stage; neither Qt nor a compiler is needed on the deployment host.

Both services bind only to their `BBSC_SERVER_IP`. If they have different addresses, set
`BBSC_SHADNET_IP` in the game-server container to shadNet's reachable IPv4 address; it defaults
to the game server's own IP. Allow these ports on the LAN/Tailscale interface:

| Protocol | Port | Service |
| --- | --- | --- |
| TCP | 31313 | shadNet login/matchmaking |
| UDP | 31314 | shadNet STUN |
| TCP | 31315 | WebAPI and Bloodborne summon broker |
| TCP | 20443 | BBSC game server and server list |
| UDP | 3478 | BBSC P2P relay |

Stats and the separate bbhost HTTP listener are disabled. The Windows DLL's TCP relay on 20444
is not started: this port uses the BBSC UDP relay on 3478.

## Player accounts

Create one account per player. The command prompts for the password without putting it into
shell history or process arguments. Use a distinct NP ID (3–16 letters/numbers/underscores/hyphens) and email per player:

```sh
docker compose exec shadnet python3 /opt/bbsc-container/server.py register HunterOne hunter1@example.com
docker compose exec shadnet python3 /opt/bbsc-container/server.py login HunterOne
```

The registration key is generated once and kept privately in the shadNet volume; the account
command reads it automatically. Public-server accounts are not copied to this server. Account
creation and login failures return a nonzero exit status.

## Launcher settings (all players)

Enable **Play online** and **Seamless co-op (BBSC)**. For example, if the server's IP is
`100.101.102.103`:

| Setting | Value |
| --- | --- |
| Server | `100.101.102.103:31313` |
| WebAPI | `http://100.101.102.103:31315` |
| Community server | `http://100.101.102.103` |
| Account | That player's new NP ID and password |
| UPnP | Off when using Tailscale |

Use the same server on every PC. The host rings the Hunt Bell; guests ring the Kin Bell.
The launcher generates the game's host overrides from these addresses. If a player previously
created `user/host_overrides.custom.json`, that file overrides the launcher settings and must
also point to this server. `BB_BBSC_LOCAL_SERVER=0` in the launcher's extra environment variables
disables its automatic local game-server fallback if you want connection failures to be visible.

## Data and updates

`shadnet-data` stores accounts, database files, the signup key, and server configuration.
`game-data` stores shared messages, bloodstains, game-server data and logs. Both are named volumes;
recreating/updating the images retains them. The generated `shadnet.cfg` is rewritten from the
container settings at startup; existing `worlds.cfg` and `scoreboards.cfg` are preserved.
Volume mounts request private SELinux labels with `:Z` on Fedora.

Stop with `docker compose down`. Do not add `-v` unless you intend to delete the accounts and
shared data. Back up both volumes while the services are stopped before moving or upgrading.
Changing `BBSC_SERVER_IP` requires recreating the containers with `docker compose up -d`.

## Podman without a Compose provider

After loading the images, this also runs both services directly (substitute your own IP):

```sh
export BBSC_SERVER_IP=100.101.102.103
podman run -d --init --name bbsc-shadnet --network host --restart unless-stopped \
  -e BBSC_SERVER_IP -v bbsc-shadnet-data:/data:Z localhost/bbsc-shadnet:0.6-pre1
podman run -d --init --name bbsc-gameserver --network host --restart unless-stopped \
  -e BBSC_SERVER_IP -v bbsc-game-data:/data:Z localhost/bbsc-gameserver:0.6-pre1
podman exec -it bbsc-shadnet python3 /opt/bbsc-container/server.py register HunterOne hunter1@example.com
```

Use this layout or Compose for a given server: they bind the same ports. Stop these containers
with `podman stop bbsc-gameserver bbsc-shadnet`; their named volumes retain the data.

## Source and checks

shadNet is built from [Wozzardman/shadnet-p2p](https://github.com/Wozzardman/shadnet-p2p), revision
`5a849a192fd4450593c57b10697316ac324c856e`, with its pinned protobuf submodule. The upstream summon
broker test runs during image construction. `SHADNET_REV` is an explicit build argument for
intentional upgrades; the default remains pinned. The account helper checks the pinned sample
tool's acknowledgement because that tool itself returns zero even on rejected replies.
`account-stdin.patch` lets that tool read the password and registration key from a private pipe.
The prebuilt archive also includes the pinned shadNet and protobuf sources in
`source/shadnet-p2p.tar.gz`; the Dockerfile records the patch and build commands.

The game server comes from this repository's `scripts/bbsc_gameserver` (BBSC/NoDreamForHunter;
its license and notices are included). Images start as root so Unraid can run its Tailscale
hook; the application helper drops supplementary groups and runs BBSC as UID/GID 99:100.
Startup assigns `/data` to 99:100 and migrates files owned by the previous image's UID 10001,
without following symlinks or changing `.tailscale_state`. Existing 10001-owned data needs one
startup as root for migration. Do not override the container user to 99:100 when using the hook.
shadNet's database is created beside its executable, so startup refreshes a copy of the binary
inside its volume. Tailscale 1.104.1 is bundled with its license and a verified download hash;
Unraid supplies and runs its own hook before the BBSC entrypoint. Tailscale does not start on
ordinary Docker/Podman runs unless a hook or sidecar starts it.

Run the packaging tests from the repository or extracted archive root:

```sh
python3 -m unittest discover -s tests -p test_bbsc_container.py
```

Health checks cover the TCP listeners, WebAPI, server-list response, and both UDP STUN services.
They do not prove that two real game clients can complete a co-op session.
