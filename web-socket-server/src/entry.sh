#!/bin/sh

set -ex

cmd="$@"

until true; do
  >&2 echo "database controller is unavailable - sleeping"
  sleep 1
done


>&2 echo "database controller is up - executing command"
exec $cmd
