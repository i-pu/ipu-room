#!/bin/bash
set -ex

./helm3-alpha uninstall server || true
docker build -t kafuhamada/web-socket-server web-socket-server/src/
docker build -t kafuhamada/database_controller database_controller

./helm3-alpha install \
-f helm/server/values.yaml \
-f helm/server/values.local.yaml \
server helm/server
