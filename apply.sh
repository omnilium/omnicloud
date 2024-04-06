#!/usr/bin/env bash

set -eo pipefail

declare -A nodes
nodes["talos-master-1"]=10.0.0.2
nodes["talos-master-2"]=10.0.0.9
nodes["talos-master-3"]=10.0.0.10
nodes["talos-worker-1"]=10.0.0.3
nodes["talos-worker-2"]=10.0.0.4
nodes["talos-worker-3"]=10.0.0.5
nodes["talos-worker-4"]=10.0.0.6
nodes["talos-worker-5"]=10.0.0.7
nodes["talos-worker-6"]=10.0.0.8

if [[ -z "$1" ]]; then
    echo "Usage: $0 <hostname>|all [flags]"
    exit 1
fi

if [[ "$1" == "all" ]]; then
  for node in "${!nodes[@]}"; do
    ./apply.sh $node ${nodes[$node]} "${@:2}"
  done

  exit 0
fi

talosctl apply-config \
  --nodes ${nodes[$1]} \
  --file rendered/$1.yaml \
  "${@:2}"
