#!/usr/bin/env bash

set -eo pipefail

declare -A nodes
nodes["talos-master-1"]=controlplane
nodes["talos-master-2"]=controlplane
nodes["talos-master-3"]=controlplane
nodes["talos-worker-1"]=worker
nodes["talos-worker-2"]=worker
nodes["talos-worker-3"]=worker
nodes["talos-worker-4"]=worker
nodes["talos-worker-5"]=worker
nodes["talos-worker-6"]=worker

if [[ -z "$1" ]]; then
  echo "Usage: $0 <hostname>|all [flags]"
  exit 1
fi

if [[ "$1" == "all" ]]; then
  for node in "${!nodes[@]}"; do
    ./render.sh $node "${@:2}"
  done

  exit 0
fi

talosctl gen config \
  --output rendered/$1.yaml \
  --output-types ${nodes[$1]} \
  --with-cluster-discovery=false \
  --with-secrets secrets.yaml \
  --config-patch @patches/ca.yaml \
  --config-patch @patches/cluster-name.yaml \
  --config-patch @patches/discovery.yaml \
  --config-patch @patches/drbd.yaml \
  --config-patch @patches/image.yaml \
  --config-patch @patches/kubelet-certificate-rotation.yaml \
  --config-patch @patches/metrics.yaml \
  --config-patch @patches/nameservers.yaml \
  --config-patch @patches/time.yaml \
  --config-patch @nodes/$1.yaml \
  --force \
  omnicloud \
  https://api.talos.omnilium.local:6443 \
  "${@:2}"
