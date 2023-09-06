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
        python3-pip \
        mosquitto-clients \
	iputils-ping \
	dnsutils \
        jq \
	wget \
        vim && \
    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list && \
    apt update && \
    TZ="America/Sao_Paulo" apt -y install mongodb-org && \  
    pip install pymongo psutil pydantic
   

FROM base as builder
RUN apt install -y  \ 
        cargo \
        build-essential \
        git \
	gcc \
	g++ \
	cmake \
	libsctp-dev && \
    	git clone https://github.com/aligungr/UERANSIM && \
    	cd UERANSIM && make && chmod a+x build/nr-binder && \
        cd .. && \
        git clone https://github.com/opensource-3d-p/rperf.git && \
        cd rperf && \
        cargo build --release && \
        cd .. && \
        git clone https://github.com/esnet/iperf.git && \
        cd iperf && \
        ./configure -bindir=/bin --enable-static-bin ; make; make install

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

