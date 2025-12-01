FROM ubuntu:24.04@sha256:440dcf6a5640b2ae5c77724e68787a906afb8ddee98bf86db94eea8528c2c076 AS base
RUN apt update && apt -y install qemu-system-x86
WORKDIR /app
ADD --chmod=444 images/bzImage .
ADD --chmod=444 images/rootfs.cpio .
ADD --chmod=555 images/run.sh ./run

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=300 JAIL_CPU=500 JAIL_MEM=512M JAIL_POW=12000 JAIL_CONNS_PER_IP=2