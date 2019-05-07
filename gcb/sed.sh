#!/bin/bash

set -ex

projectid=$1
dockerusername=$2
tag=$3

image=$1-server

sed -e 's/PROJECT_ID/${projectid}/g' server-pod.yaml
sed -e 's/DOCKER_USERNAME/${dockerusername}/g' server-pod.yaml
sed -e 's/IMAGE/${image}/g' server-pod.yaml
sed -e 's/TAG/${tag}/g' server-pod.yaml
