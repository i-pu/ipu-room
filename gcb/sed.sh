#!/bin/bash

set -ex

projectid=$1
dockerusername=$2
tag=$3

image=$1-server
curDir=$(cd $(dirname $0);pwd)
filepath=${curDir}/kube/server-pod.yaml

sed -i s/PROJECT_ID/${projectid}/g ${filepath}
sed -i s/DOCKER_USERNAME/${dockerusername}/g ${filepath}
sed -i s/IMAGE/${image}/g ${filepath}
sed -i s/TAG/${tag}/g ${filepath}
