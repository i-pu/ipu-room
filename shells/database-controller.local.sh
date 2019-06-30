#!/bin/bash

set -ex

cd $(cd $(dirname $0);pwd)
cd ..

./helm3-alpha uninstall database-controller || true
docker build -t kafuhamada/ipu-database-controller database-controller

./helm3-alpha install \
-f helm/values.yaml \
-f helm/database-controller/values.yaml \
database-controller helm/database-controller
