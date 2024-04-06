#!/usr/bin/env bash

set -eo pipefail

if [[ -z "$1" ]]; then
  echo "Usage: $0 <hostname>|all [type] [flags]"
  exit 1
fi

if [[ "$1" == "all" ]]; then
  declare -A nodes
  nodes["talos-master-1"]=controlplane
  nodes["talos-worker-1"]=worker
  nodes["talos-worker-2"]=worker
  nodes["talos-worker-3"]=worker
  nodes["talos-worker-4"]=worker
  nodes["talos-worker-5"]=worker
  nodes["talos-worker-6"]=worker

  for node in "${!nodes[@]}"; do
    ./render.sh $node ${nodes[$node]} "${@:2}"
  done

  exit 0
fi

TYPE=${2:-worker}

talosctl gen config \
  --output rendered/$1.yaml \
  --output-types $TYPE \
  --with-cluster-discovery=false \
  --with-secrets secrets.yaml \
  --config-patch @patches/ca.yaml \
  --config-patch @patches/cluster-name.yaml \
  --config-patch @patches/discovery.yaml \
  --config-patch @patches/kubelet-certificate-rotation.yaml \
  --config-patch @patches/mayastor.yaml \
  --config-patch @patches/metrics.yaml \
  --config-patch @nodes/$1.yaml \
  --force \
  omnicloud \
  https://api.talos.omnilium.local:6443 \
  "${@:3}"
