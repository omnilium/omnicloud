#!/usr/bin/env bash

set -eo pipefail

sops -d -i secrets.yaml
sops -d -i patches/harbor.yaml
