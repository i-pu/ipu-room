#!/bin/bash
set -ex

./helm3-alpha uninstall web-socket-server || true
docker build -t kafuhamada/web-socket-server web-socket-server/src/

./helm3-alpha install \
-f helm/values.yaml \
-f helm/web-socket-server/values.yaml \
web-socket-server helm/web-socket-server
