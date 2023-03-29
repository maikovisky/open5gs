FROM alpine:latest as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
RUN apk update && \
    apk add --no-cache \
       bash \
       iproute2 \
       iperf \
       curl \
       prometheus-node-exporter 

WORKDIR /



