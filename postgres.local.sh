#!/bin/bash
set -ex

./helm3-alpha uninstall postgres || true

./helm3-alpha install \
-f helm/values.yaml \
-f helm/postgres/values.yaml \
postgres helm/postgres
