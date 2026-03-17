# Stage 1: Base image with shared environment variables
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/opt/venv" \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Stage 2: Build dependencies
FROM base AS deps
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copying only dependency files first leverages Docker caching
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 3: Runtime
FROM base AS runtime
# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the virtualenv and app code
COPY --from=deps /opt/venv /opt/venv
COPY . .

# Ensure the appuser owns the /app directory
RUN chown -R appuser:appuser /app &&\
    chmod +x /app/prestart.sh

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Use a startup script to handle migrations before launching the app
CMD ["/bin/bash", "prestart.sh"]