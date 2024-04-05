#!/usr/bin/env bash

set -eo pipefail

sops -d -i secrets.yaml
sops -d -i --input-type yaml --output-type yaml talosconfig
