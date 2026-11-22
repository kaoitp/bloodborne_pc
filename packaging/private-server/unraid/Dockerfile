ARG BASE_IMAGE=ghcr.io/kaoitp/bloodborne-private-server@sha256:d3afb1b12dd2cf3b302f1dce4394e20a6ca1982d591a9c33baa4d192f956c45c
FROM debian:trixie-slim AS fetch

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
    && curl -fsSL --retry 3 https://pkgs.tailscale.com/stable/tailscale_1.104.7_amd64.tgz -o /tmp/tailscale.tgz \
    && echo 'e56693ff74a64f2591b7e819c280635a100aae1ddfb0ef058fcd052b7cd8d16c  /tmp/tailscale.tgz' | sha256sum -c - \
    && tar -xzf /tmp/tailscale.tgz -C /tmp \
    && curl -fsSL --retry 3 https://raw.githubusercontent.com/tailscale/tailscale/cbc74fe48ef1b1649f69a4d9a602319427e25102/LICENSE -o /tmp/tailscale.LICENSE \
    && echo 'a7ca6186a7963a0a60740f6047760eecd7a0234e8c38bd7e1e0bbcb324bda45b  /tmp/tailscale.LICENSE' | sha256sum -c -

FROM ${BASE_IMAGE}

LABEL org.opencontainers.image.title="Bloodborne PC private Seamless co-op server for Unraid Tailscale" \
      org.opencontainers.image.licenses="GPL-2.0-or-later AND BSD-3-Clause"

# Unraid invokes its hook as the image's user before it runs this entrypoint.
USER root
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates gosu jq \
    && rm -rf /var/lib/apt/lists/*
COPY --from=fetch /tmp/tailscale_1.104.7_amd64/tailscale /tmp/tailscale_1.104.7_amd64/tailscaled /usr/bin/
COPY --from=fetch /tmp/tailscale.LICENSE /usr/share/doc/tailscale/copyright

ENTRYPOINT ["gosu", "10001:10001", "/usr/bin/tini", "--", "/usr/local/bin/shadnet-start"]
