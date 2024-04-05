#!/usr/bin/env bash

set -eo pipefail

if [[ -z "$1" ]]; then
    echo "Usage: $0 <hostname>"
    exit 1
fi

TYPE=${2:-worker}

if [[ "$TYPE" == "worker" ]]; then
  talosctl gen config \
    --output rendered/$1.yaml \
    --output-types $TYPE \
    --with-cluster-discovery=false \
    --with-secrets secrets.yaml \
    --config-patch @patches/cluster-name.yaml \
    --config-patch @patches/mayastor.yaml \
    --config-patch @nodes/$1.yaml \
    --force \
    omnicloud \
    https://api.talos.omnilium.local:6443 \
    "${@:3}"
else
  talosctl gen config \
    --output rendered/$1.yaml \
    --output-types $TYPE \
    --with-cluster-discovery=false \
    --with-secrets secrets.yaml \
    --config-patch @patches/cluster-name.yaml \
    --config-patch @nodes/$1.yaml \
    --force \
    omnicloud \
    https://api.talos.omnilium.local:6443 \
    "${@:3}"
fi
