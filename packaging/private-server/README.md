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

To install from the Docker image archive attached to the release, download it to the Docker host and run the following commands. This works without a registry login.

```sh
docker load -i bloodborne-private-server-1.9.8.6-linux-amd64.tar.gz
docker compose up -d --pull never
```

Compose keeps the server database, worlds, and `link_key.bin` in `server-data`. Keep this data when upgrading or backing up. If using an Unraid appdata bind mount for `/data`, give UID and GID `10001` write access to that directory.

## Unraid template

The [Unraid XML template](unraid/my-bloodborne-private-server.xml) uses `bridge`, the `latest` image, and the same three ports on the Unraid host. Run these commands in the Unraid terminal to import it and prepare the default appdata directory.

```sh
mkdir -p /boot/config/plugins/dockerMan/templates-user
curl -fL https://raw.githubusercontent.com/kaoitp/bloodborne_pc/private-server/packaging/private-server/unraid/my-bloodborne-private-server.xml \
  -o /boot/config/plugins/dockerMan/templates-user/my-bloodborne-private-server.xml
install -d -m 0750 -o 10001 -g 10001 /mnt/user/appdata/bloodborne-private-server
```

In Unraid, open **Docker → Add Container** and select **Bloodborne-Private-Server** under **Template**. Keep the default ports, then click **Apply**. To pin the release, set **Repository** to `ghcr.io/kaoitp/bloodborne-private-server:1.9.8.6`.

Players connect to the Unraid LAN IPv4, or to the Unraid host's Tailscale IPv4 when using the [Tailscale plugin](https://docs.unraid.net/unraid-os/system-administration/secure-your-server/tailscale/). The game listens on the host's published ports. Keep those ports within your LAN or Tailnet and leave router port forwarding off. To check the host, open `http://<unraid-ip>:20443/status` from a player PC.

## Unraid Tailscale hook

Use the [Tailscale XML template](unraid/my-bloodborne-private-server-tailscale.xml) for a distinct container on your Tailnet. It uses the official Unraid **Use Tailscale** hook with Bridge and kernel networking, and publishes no host ports. The image comes with the Tailscale binaries. The hook starts as root and the game server starts as UID/GID `10001:10001`.

```sh
mkdir -p /boot/config/plugins/dockerMan/templates-user
curl -fL https://raw.githubusercontent.com/kaoitp/bloodborne_pc/private-server/packaging/private-server/unraid/my-bloodborne-private-server-tailscale.xml \
  -o /boot/config/plugins/dockerMan/templates-user/my-bloodborne-private-server-tailscale.xml
install -d -m 0750 -o 10001 -g 10001 /mnt/user/appdata/bloodborne-private-server
```

Stop any existing Bloodborne host that uses that appdata directory before starting the new container. In **Docker → Add Container**, select **Bloodborne-Private-Server-Tailscale**. Leave **Use Tailscale** on and **Tailscale Userspace Networking** disabled. After clicking **Apply**, open its log and follow the Tailscale authorization link once. The authorization persists in `/data/.tailscale_state`.

Give players the container's Tailscale IPv4. Its Tailnet access policy must permit UDP `31314` and TCP `31315` and `20443`. From a player PC, check `http://<container-tailscale-ip>:20443/status`, then enter that IPv4 under **Private server** in the launcher. The image is `ghcr.io/kaoitp/bloodborne-private-server-tailscale:latest`. Use the tag `1.9.8.6` to pin this release.

## Version and source

The image tag follows the SuperMedo Windows version. The server checks the BBSC release reported by the Seamless engine, which is `1.0.0` in Windows 1.9.8.6. The [BBSC 1.0.0 Linux server source archive](https://github.com/CLSAMG22/BBSC/releases/download/v1.0.0/BBSC-Yharnam-Together-1.0.0-Server-Linux.zip) and the [pinned protobuf source](https://github.com/shadexternals/protobuf/tree/5917ee224a7e47383a78acc129628511fe210dff) are used by the [Dockerfile](Dockerfile). Build locally with `docker build -t bloodborne-private-server:1.9.8.6 .` from this directory.
