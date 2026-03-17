#!/bin/bash

set -e

cd /app/backend

echo "Waiting for database migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
exec fastapi dev main.py --host 0.0.0.0 --port 8000