#!/bin/bash
set -ex

./helm3-alpha uninstall database-controller || true
docker build -t kafuhamada/database-controller database-controller

./helm3-alpha install \
-f helm/values.yaml \
-f helm/database-controller/values.yaml \
database-controller helm/database-controller