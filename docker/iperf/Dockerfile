FROM ubuntu:jammy as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
RUN apt update && \
    apt upgrade -y && \
    apt install -y curl \
        bash \
        prometheus-node-exporter \
        net-tools \
        iproute2 \
        iptables \
        iperf3 \
        iperf \
        mosquitto \
        iputils-ping \
        dnsutils \
        vim


WORKDIR /



