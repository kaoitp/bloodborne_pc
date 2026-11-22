#!/bin/sh
set -eu

image=${1:?Pass the image name to test}
container="bbsc-smoke-$$"
volume=$(docker volume create)
cleanup() {
    docker logs "$container" 2>&1 || true
    docker rm -f "$container" >/dev/null 2>&1 || true
    docker volume rm "$volume" >/dev/null
}
trap cleanup EXIT

start() {
    docker run --detach --name "$container" --mount "source=$volume,target=/data" "$image" >/dev/null
    for _ in $(seq 1 30); do
        if docker exec "$container" curl -fsS http://127.0.0.1:20443/status >/dev/null 2>&1 &&
           docker exec "$container" curl -fsS http://127.0.0.1:31315/status >/dev/null 2>&1; then
            return
        fi
        if [ "$(docker inspect --format '{{.State.Running}}' "$container")" != true ]; then
            break
        fi
        sleep 1
    done
    return 1
}

start
docker logs "$container" 2>&1 | grep -E 'bb-build 1;version=1\.0\.0;.*protocol=9;'
docker exec "$container" grep -q ':7A52 ' /proc/net/udp # 31314/udp
docker exec "$container" sh -c 'test "$(id -u)" = 10001 && test -s /data/db/shadnet.db && test -s /data/link_key.bin'
first_key=$(docker exec "$container" sha256sum /data/link_key.bin)
docker stop "$container" >/dev/null
docker rm "$container" >/dev/null
start
test "$(docker exec "$container" sha256sum /data/link_key.bin)" = "$first_key"
echo 'BBSC services, release fingerprint, non-root user and persistent server key passed.'
