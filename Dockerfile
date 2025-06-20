# syntax=docker/dockerfile:1

########################
# Stage 1 – builder   #
########################
FROM ghcr.io/astral-sh/uv:debian-slim AS builder

# Turn off interactive prompts & set working dir
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Copy dependency descriptors first for better layer caching
COPY pyproject.toml uv.lock ./

# Install only third-party deps (no project code yet)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable --compile-bytecode

# Copy the rest of the source code
COPY . .

# Install project itself into the venv (still using uv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-editable --compile-bytecode

########################
# Stage 2 – runtime    #
########################
FROM python:3.12-slim AS runtime

# Copy the virtualenv created in the builder layer
COPY --from=builder /app/.venv /app/.venv

# Copy uv binary so we can use `uv run` in production
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Bring project code (resources etc.)
COPY --from=builder /app /app

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Default command — same as you run locally
CMD ["uv", "run", "src/server.py"] 