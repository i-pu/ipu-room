#!/bin/bash
set -ex
docker-compose up -d
echo "DATABASE_URL=postgresql://postgres:password@localhost:5432/plugin_market
RUST_LOG=actix_web=debug" > .env
diesel migration run
