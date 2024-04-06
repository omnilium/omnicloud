#!/usr/bin/env bash

set -eo pipefail

sops -e -i secrets.yaml
sops -e -i patches/harbor.yaml
