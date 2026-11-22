FROM debian:trixie-slim AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates cmake curl g++ git ninja-build qt6-base-dev \
    qt6-httpserver-dev qt6-websockets-dev unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
# BBSC 1.0.0 is the release advertised by the Windows Seamless engine.
RUN curl --fail --silent --show-error --location --retry 3 \
    https://github.com/CLSAMG22/BBSC/releases/download/v1.0.0/BBSC-Yharnam-Together-1.0.0-Server-Linux.zip \
    -o /tmp/bbsc.zip \
    && echo '737dfbb69b2b90c2916f041ddeaed081614140d79aa003617b1a67bd84ce25aa  /tmp/bbsc.zip' | sha256sum -c - \
    && unzip -p /tmp/bbsc.zip '*/bbsc-yharnam-together-server-src-1.0.0.tar.gz' > /tmp/bbsc.tar.gz \
    && tar -xzf /tmp/bbsc.tar.gz \
    && rm /tmp/bbsc.zip /tmp/bbsc.tar.gz

RUN git -C externals/protobuf init \
    && git -C externals/protobuf fetch --depth 1 https://github.com/shadexternals/protobuf.git 5917ee224a7e47383a78acc129628511fe210dff \
    && git -C externals/protobuf checkout --detach FETCH_HEAD \
    && cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF \
        -DBLOODBORNE_SS_INFO_TEMPLATE=/src/_backend/ss_info_template.xml \
    && cmake --build build --target shadnet --parallel 3 \
    && strip build/shadnet

FROM debian:trixie-slim

ARG PORT_VERSION=1.9.8.6
LABEL org.opencontainers.image.title="Bloodborne PC private Seamless co-op server" \
      org.opencontainers.image.version="${PORT_VERSION}" \
      org.opencontainers.image.licenses="GPL-2.0-or-later" \
      org.opencontainers.image.source="https://github.com/kaoitp/bloodborne_pc"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl libqt6concurrent6 libqt6httpserver6 libqt6sql6-sqlite tini \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 shadnet \
    && useradd --uid 10001 --gid 10001 --home-dir /data --shell /usr/sbin/nologin shadnet \
    && install -d -m 0750 -o shadnet -g shadnet /data

COPY --from=build /src/build/shadnet /usr/local/bin/shadnet
COPY --from=build /src/worlds.cfg /src/scoreboards.cfg /opt/shadnet/
COPY --from=build /src/LICENSES /usr/share/doc/shadnet/licenses/
COPY --from=build /src/externals/protobuf/LICENSE /usr/share/doc/shadnet/licenses/protobuf.txt
COPY --chmod=755 entrypoint.sh /usr/local/bin/shadnet-start

ENV SHADNET_HOME=/data BB_RELEASE_VERSION=1.0.0
WORKDIR /data
VOLUME /data
USER 10001:10001
EXPOSE 31314/udp 31315/tcp 20443/tcp
HEALTHCHECK --interval=10s --timeout=4s --start-period=10s \
    CMD curl --fail --silent --max-time 3 http://127.0.0.1:20443/status || exit 1
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/shadnet-start"]
