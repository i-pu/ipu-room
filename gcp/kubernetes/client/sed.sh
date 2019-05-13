#!/bin/bash
set -eX

dockerusername=$1
tag=$2

image=$1-server
curDir=$(cd $(dirname $0);pwd)
filepath=${curDir}/deployment.yaml

sed -i s/DOCKER_USERNAME/${dockerusername}/g ${filepath}
sed -i s/TAG/${tag}/g ${filepath}
