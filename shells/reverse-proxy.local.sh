#!/bin/bash

set -ex

cd ..

./helm3-alpha uninstall reverse-proxy || true

./helm3-alpha install \
-f helm/values.yaml \
reverse-proxy helm/reverse-proxy
