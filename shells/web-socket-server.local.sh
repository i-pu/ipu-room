#!/bin/bash

set -ex

cd ..

./helm3-alpha uninstall web-socket-server || true
docker build -t kafuhamada/ipu-web-socket-server web-socket-server/src/

./helm3-alpha install \
-f helm/values.yaml \
-f helm/web-socket-server/values.yaml \
web-socket-server helm/web-socket-server
