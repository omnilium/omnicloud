#!/usr/bin/env bash

set -eo pipefail

sops -e -i secrets.yaml
