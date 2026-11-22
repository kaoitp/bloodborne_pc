# Bloodborne PC private Seamless Co-op

The [Windows launcher release](https://github.com/kaoitp/bloodborne_pc/releases) adds a **Private server** option under **Seamless Co-op**. Apply the launcher ZIP to a copy of the official SuperMedo Windows release with the same version. The [ZIP instructions](INSTALL.txt) describe which files to replace.

## Start the host

Run the Compose file on a Linux or Unraid Docker host. Set `HOST_IP` in a `.env` file to the host's LAN IPv4 or its Tailscale IPv4. Set `SERVER_TAG=1.9.8.6` to stay on the matching Windows release. Compose uses `latest` when `SERVER_TAG` is absent.

```dotenv
HOST_IP=100.64.0.10
SERVER_TAG=1.9.8.6
```

```sh
docker compose up -d
docker compose ps
```

The `linux/amd64` image is `ghcr.io/kaoitp/bloodborne-private-server`. The Compose file publishes `31314/udp`, `31315/tcp`, and `20443/tcp` on `HOST_IP`. For Tailscale, connect the Docker host and each player to a Tailnet that permits these ports. Give the same `HOST_IP` to every player. Each player selects **Private server**, enters that address, and uses **F2** in the game to create or join the team.

Compose keeps the server database, worlds, and `link_key.bin` in `server-data`. Keep this data when upgrading or backing up. If using an Unraid appdata bind mount for `/data`, give UID and GID `10001` write access to that directory.

## Version and source

The image tag follows the SuperMedo Windows version. The server checks the BBSC release reported by the Seamless engine, which is `1.0.0` in Windows 1.9.8.6. The [BBSC 1.0.0 Linux server source archive](https://github.com/CLSAMG22/BBSC/releases/download/v1.0.0/BBSC-Yharnam-Together-1.0.0-Server-Linux.zip) and the [pinned protobuf source](https://github.com/shadexternals/protobuf/tree/5917ee224a7e47383a78acc129628511fe210dff) are used by the [Dockerfile](Dockerfile). Build locally with `docker build -t bloodborne-private-server:1.9.8.6 .` from this directory.
