#!/usr/bin/env bash

set -eo pipefail

sops -e -i secrets.yaml
sops -e -i --input-type yaml --output-type yaml talosconfig
