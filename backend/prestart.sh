#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Waiting for database migrations..."
# Run migrations to create/update tables
alembic upgrade head

echo "Starting FastAPI server..."
# Use 'run' for production-style serving (provided by fastapi-cli)
exec fastapi run main.py --host 0.0.0.0 --port 8000