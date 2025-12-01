# syntax=docker/dockerfile:1
# check=error=true

ARG GO_VERSION=1.24
ARG DISTRO=-alpine

################################################################################
FROM golang:${GO_VERSION}${DISTRO} AS builder

WORKDIR /app
ENV CGO_ENABLED=0

RUN \
  --mount=type=bind,src=go.mod,dst=go.mod \
  --mount=type=bind,src=main.go,dst=main.go \
  go build -o log-viewer -ldflags='-s -w' -trimpath -x .

################################################################################
FROM scratch
ARG PORT=9999

WORKDIR /app
COPY --from=builder /app/log-viewer /usr/local/bin/
COPY ./logs ./logs

EXPOSE ${PORT}
ENTRYPOINT ["/usr/local/bin/log-viewer"]
