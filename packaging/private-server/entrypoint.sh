#!/bin/sh
set -eu

umask 027
cd "$SHADNET_HOME"
mkdir -p db backend bloodborne_worlds

for file in worlds.cfg scoreboards.cfg; do
    if [ ! -f "$file" ]; then
        cp "/opt/shadnet/$file" "$file"
    fi
done

if [ ! -f shadnet.cfg ]; then
    cat > shadnet.cfg <<'EOF'
[General]
Host=0.0.0.0
TcpLocalOnly=true
MatchingUdpPort=31314
WebApiPort=31315
StatsEnabled=false
BloodborneSeamlessCoop=true
BloodborneBackend=true
BackendPort=20443
BackendFolder=backend
BackendStore=db/backend.db
Hosted=false
MakeAccountsAtSignIn=true
CheckServerBuild=true
EOF
fi

exec shadnet "$@"
