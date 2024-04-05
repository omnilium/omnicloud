#!/usr/bin/env bash

set -eo pipefail

if [[ -z "$1" ]]; then
    echo "Usage: $0 <hostname> <address>"
    exit 1
fi

if [[ -z "$2" ]]; then
    echo "Usage: $0 <hostname> <address>"
    exit 1
fi

talosctl apply-config \
  --nodes $2 \
  --file rendered/$1.yaml \
  "${@:3}"
