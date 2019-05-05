#!/bin/sh

set -ex

cmd="$@"

# hide password from stdout
set +ex
export PGPASSWORD=$POSTGRES_PASSWORD
set -ex

until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -w -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done


>&2 echo "Postgres is up - executing command"
exec $cmd
