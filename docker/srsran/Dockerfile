FROM ubuntu:jammy as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install -y curl \
        gdb \
	prometheus-node-exporter \
	gnupg \
	libsctp1 \
	lksctp-tools \
	libmongoc-1.0-0 \
	net-tools \
	iproute2 \
	iptables \
	iperf \
	netperf \
        python3-pip \
        mosquitto-clients \
	iputils-ping \
	dnsutils \
        jq \
	wget \
        vim && \
    pip install pymongo psutil pydantic
   

FROM base as builder
RUN apt install -y  \ 
        build-essential \
        git \
	gcc \
	g++ \
	cmake \
        make \
	libsctp-dev && \
        libzmq3-dev && \
        libtool && \
        pkg-config libfftw3-dev libmbedtls-dev libyaml-cpp-dev libgtest-dev && \
   git clone https://github.com/zeromq/czmq.git  && \
   cd czmq  && \
   ./autogen.sh  && \
   ./configure  && \
   make  && \
   make install && \
   ldconfig && \
   git clone https://github.com/srsran/srsRAN_Project.git && \
   cd srsRAN_Project && \
   mkdir build && cd build && \
   cmake ../ -DENABLE_EXPORT=ON -DENABLE_ZEROMQ=ON && \
   make  -j`nproc` && \
   make install

WORKDIR /


FROM base as final
RUN mkdir -p /var/log/ueransim 

WORKDIR /
COPY --from=builder /UERANSIM/build/nr-gnb /bin
COPY --from=builder /UERANSIM/build/nr-ue /bin
COPY --from=builder /UERANSIM/build/nr-cli /bin
COPY --from=builder /UERANSIM/build/nr-binder /bin
COPY --from=builder /UERANSIM/build/libdevbnd.so /lib
COPY --from=builder /UERANSIM/config /etc/ueransim
COPY --from=builder /rperf/target/release/rperf  /bin
COPY --from=builder /iperf/src/iperf3 /bin
COPY etc /etc
COPY bin /bin

