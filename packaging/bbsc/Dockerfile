FROM docker.io/library/fedora:44 AS tailscale
RUN dnf install -y --setopt=install_weak_deps=False curl-minimal tar gzip && dnf clean all
ARG TAILSCALE_VERSION=1.104.1
ARG TAILSCALE_SHA256=108d1d96ecf410d305571e173516f27038f870919a9b89c914a167c6d33a4528
RUN curl -fL --retry 3 -o /tmp/tailscale.tgz "https://pkgs.tailscale.com/stable/tailscale_${TAILSCALE_VERSION}_amd64.tgz" \
    && echo "${TAILSCALE_SHA256}  /tmp/tailscale.tgz" | sha256sum -c - \
    && tar -xzf /tmp/tailscale.tgz -C /tmp \
    && install -D -m755 /tmp/tailscale_${TAILSCALE_VERSION}_amd64/tailscale /install/bin/tailscale \
    && install -D -m755 /tmp/tailscale_${TAILSCALE_VERSION}_amd64/tailscaled /install/bin/tailscaled \
    && install -d /install/licenses \
    && curl -fL --retry 3 -o /install/licenses/LICENSE "https://raw.githubusercontent.com/tailscale/tailscale/v${TAILSCALE_VERSION}/LICENSE"

FROM docker.io/library/fedora:44 AS base
RUN dnf install -y --setopt=install_weak_deps=False python3 jq iptables iproute ca-certificates && dnf clean all \
    && groupadd -f --gid 100 users \
    && useradd --system --uid 99 --gid 100 --no-create-home bbsc \
    && install -d -o 99 -g 100 /data
COPY --from=tailscale /install/bin/ /usr/bin/
COPY --from=tailscale /install/licenses/ /usr/share/licenses/tailscale/
COPY packaging/bbsc/server.py /opt/bbsc-container/server.py
WORKDIR /data
ENTRYPOINT ["python3", "/opt/bbsc-container/server.py"]

FROM base AS gameserver
COPY scripts/bbsc_gameserver/bbsc_gameserver.py scripts/bbsc_gameserver/bbhost_service.py \
    scripts/bbsc_gameserver/ss_info_template.xml scripts/bbsc_gameserver/NOTICE.txt \
    scripts/bbsc_gameserver/LICENSE.NoDreamForHunter /opt/bbsc-gameserver/
USER 0:0
CMD ["gameserver"]

FROM docker.io/library/fedora:44 AS build
RUN dnf install -y --setopt=install_weak_deps=False git cmake ninja-build gcc-c++ \
    qt6-qtbase-devel qt6-qthttpserver-devel && dnf clean all
ARG SHADNET_REV=5a849a192fd4450593c57b10697316ac324c856e
RUN git init /src && cd /src \
    && git remote add origin https://github.com/Wozzardman/shadnet-p2p.git \
    && git fetch --depth 1 origin "$SHADNET_REV" && git checkout --detach FETCH_HEAD \
    && git submodule update --init --recursive --depth 1
WORKDIR /src
COPY packaging/bbsc/account-stdin.patch /tmp/account-stdin.patch
RUN git apply /tmp/account-stdin.patch \
    && printf '\nadd_subdirectory(clientsample)\nset_property(TARGET shadnet-sample PROPERTY LINK_OPTIONS "")\n' >> CMakeLists.txt
RUN --mount=type=cache,id=bbsc-shadnet-build,target=/src/build \
    cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=ON \
    && cmake --build build --parallel 4 --target shadnet shadnet-sample test_bloodborne_summon_broker \
    && ctest --test-dir build --output-on-failure \
    && install -d /install \
    && install -m755 build/shadnet build/clientsample/shadnet-sample /install/ \
    && install -m644 build/worlds.cfg build/scoreboards.cfg /install/ \
    && strip /install/shadnet /install/shadnet-sample

FROM base AS shadnet
RUN dnf install -y --setopt=install_weak_deps=False qt6-qtbase \
    qt6-qthttpserver && dnf clean all
COPY --from=build /install/ /opt/shadnet/
COPY --from=build /src/LICENSES /usr/share/licenses/shadnet
ARG SHADNET_REV=5a849a192fd4450593c57b10697316ac324c856e
LABEL org.opencontainers.image.source="https://github.com/Wozzardman/shadnet-p2p" \
      org.opencontainers.image.revision="${SHADNET_REV}"
USER 0:0
CMD ["shadnet"]
