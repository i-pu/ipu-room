#!/bin/bash

set -ex

cd $(cd $(dirname $0);pwd)
cd ..

./helm3-alpha uninstall client || true
docker build -t kafuhamada/ipu-client -f client/Dockerfile-cd client

./helm3-alpha install \
-f helm/values.yaml \
-f helm/client/values.yaml \
client helm/client
