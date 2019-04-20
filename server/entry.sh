#!/bin/sh

set -ex

cmd="$@"

echo -n "*:*:*:*:$POSTGRES_PASSWORD" > ~/.pgpass
chmod 600 ~/.pgpass

until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -w -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

rm -f ~/.pgpass

>&2 echo "Postgres is up - executing command"
exec $cmd
