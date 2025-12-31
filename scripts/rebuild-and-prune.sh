#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$SCRIPT_DIR"

echo "Stopping containers..."
docker compose down

echo "Rebuilding and starting containers..."
docker compose up -d --build

echo "Pruning unused images..."
docker image prune -f

echo "Rebuild and prune complete"
