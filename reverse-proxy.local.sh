#!/bin/bash

set -ex

./helm3-alpha uninstall reverse-proxy || true

./helm3-alpha install \
-f helm/values.yaml \
reverse-proxy helm/reverse-proxy
