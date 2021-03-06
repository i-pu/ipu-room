#!/bin/bash

set -ex

cd $(cd $(dirname $0);pwd)
cd ..

./helm3-alpha uninstall postgres || true

./helm3-alpha install \
-f helm/values.yaml \
-f helm/postgres/values.yaml \
postgres helm/postgres
