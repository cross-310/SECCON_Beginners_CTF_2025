# syntax=docker/dockerfile:1
# check=error=true


ARG DISTRO=slim-bookworm

################################################################################
FROM python:3.12-${DISTRO} AS base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

################################################################################
FROM base AS builder

# Create virtual environment
RUN python3 -m venv .venv

ENV PIP_ROOT_USER_ACTION=ignore
RUN --mount=type=bind,src=requirements.txt,dst=requirements.txt \
  .venv/bin/pip install --no-cache-dir -r requirements.txt

################################################################################
FROM base

ENV HOST=host.docker.internal
ENV PORT=9999

# Copy the virtual environment from the builder stage
COPY --from=builder /usr/src/app/.venv ./.venv

# Copy source code
COPY solver.py .

# Set the command to run the app
ENTRYPOINT [ ".venv/bin/python", "solver.py" ]
