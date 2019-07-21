#!/bin/bash

set -ex

cd $(cd $(dirname $0);pwd)
cd ..

./helm3-alpha uninstall backend || true
docker build -t kafuhamada/ipu-backend backend

./helm3-alpha install \
-f helm/values.yaml \
-f helm/backend/values.yaml \
backend helm/backend
