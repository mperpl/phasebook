FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/opt/venv" \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

FROM base AS deps
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM base AS runtime
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=deps /opt/venv /opt/venv
COPY . .

RUN chown -R appuser:appuser /app &&\
    chmod +x /app/prestart.sh

USER appuser

EXPOSE 8000

CMD ["/bin/bash", "prestart.sh"]