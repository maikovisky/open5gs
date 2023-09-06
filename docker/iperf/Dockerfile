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
        iperf \
        mosquitto \
        iputils-ping \
        dnsutils \
        vim

WORKDIR /

FROM base as builder 
RUN  apt install -y git \
         cargo \
         build-essential \
         make && \
     git clone https://github.com/opensource-3d-p/rperf.git && \
     cd rperf && \
     cargo build --release && \
     cd .. && \
     git clone https://github.com/esnet/iperf.git && \
     cd iperf && \
     ./configure -bindir=/bin --enable-static-bin ; make; make install 
 
WORKDIR /

FROM base as final

WORKDIR /
COPY --from=builder /rperf/target/release/rperf  /bin 
COPY --from=builder /iperf/src/iperf3 /bin


WORKDIR /


