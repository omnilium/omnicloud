#!/usr/bin/env bash

set -eo pipefail

if [[ -z "$1" ]]; then
    echo "Usage: $0 <hostname>|all [address] [flags]"
    exit 1
fi

if [[ "$1" == "all" ]]; then
  declare -A nodes
  nodes["talos-master-1"]=10.0.0.2
  nodes["talos-worker-1"]=10.0.0.3
  nodes["talos-worker-2"]=10.0.0.4
  nodes["talos-worker-3"]=10.0.0.5
  nodes["talos-worker-4"]=10.0.0.6
  nodes["talos-worker-5"]=10.0.0.7
  nodes["talos-worker-6"]=10.0.0.8

  for node in "${!nodes[@]}"; do
    ./apply.sh $node ${nodes[$node]} "${@:2}"
  done

  exit 0
fi

if [[ -z "$2" ]]; then
    echo "Usage: $0 <hostname> <address> [flags]"
    exit 1
fi

talosctl apply-config \
  --nodes $2 \
  --file rendered/$1.yaml \
  "${@:3}"
