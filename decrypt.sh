#!/usr/bin/env bash

set -eo pipefail

sops -d -i secrets.yaml
