FROM ubuntu:jammy as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y curl \
        gdb \
	prometheus-node-exporter \
	libtalloc2 \
	libmicrohttpd12 \
	libyaml-0-2 \ 
	libmongoc-1.0-0 \
	libsctp1 \
	lksctp-tools \
	libmongoc-1.0-0 \
	libidn12 \
	libtins4.0 \
	net-tools \
	iproute2 \
	iptables \
	iputils-ping \
	tcpdump \
	git \
	clang \
	cmake \
	libelf1 \
	libelf-dev \
	zlib1g-dev \
	llvm-dev \
	libbfd-dev \
        vim && \
	git clone --recurse-submodules https://github.com/maikovisky/open5gs-bpf.git  
   

FROM base as builder
RUN apt install -y python3-pip \ 
        python3-setuptools \
        python3-wheel \
        ninja-build \
        build-essential \
        flex \
        bison \
        git \
        cmake \
        libsctp-dev \
        libgnutls28-dev \
        libgcrypt-dev \
        libssl-dev \
        libidn11-dev \
        libmongoc-dev \
        libbson-dev \
        libyaml-dev \
        libnghttp2-dev \
        libmicrohttpd-dev \
        libcurl4-gnutls-dev \
        libnghttp2-dev \
        libtins-dev \
        libtalloc-dev \
        meson \
	golang-go && \
        git clone --recursive https://github.com/open5gs/open5gs && \
        cd open5gs && \
	git checkout main  && \
	meson subprojects update && \
        meson build --prefix=`pwd`/install && \
        ninja -C  build && \
        cd build && \
        ninja install && \
        cd / && \ 
	git clone https://github.com/my5G/my5G-RANTester.git && \
	cd my5G-RANTester && \
	go mod download && \
	cd cmd && \
	go build app.go 

WORKDIR /


FROM base as final
RUN mkdir -p /var/log/open5gs \
    rc-update add node-exporter default
#    echo "tun" >> /etc/modules-load.d/tun.conf && \
#    echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.d/open5gs.conf && \
#    echo "net.ipv6.conf.all.disable_ipv6=0" >> /etc/sysctl.d/open5gs.conf && \
#    echo "net.ipv6.conf.default.disable_ipv6=0" >> /etc/sysctl.d/open5gs.conf && \
#    echo "net.ipv6.conf.lo.disable_ipv6=0" >> /etc/sysctl.d/open5gs.conf && \
#    echo "net.ipv6.conf.eth0.disable_ipv6=0" >> /etc/sysctl.d/open5gs.conf && \
#    echo "auto ogstun" >> /etc/network/interfaces && \
#    echo "iface ogstun inet static" >> /etc/network/interfaces && \
#    echo "  pre-up ip tuntap add name ogstun mode tun" >> /etc/network/interfaces
#    echo "  pre-up ip addr add 10.45.0.1/16 dev ogstun" >> /etc/network/interfaces
#    echo "  pre-up ip addr add 2001:db8:cafe::1/48 dev ogstun" >> /etc/network/interfaces
#    echo "   pre-up ip link set ogstun up" >> /etc/network/interfaces

WORKDIR /
COPY --from=builder /open5gs/install/bin  /bin 
COPY --from=builder /open5gs/install/bin  /bin 
COPY --from=builder /open5gs/install/lib  /lib
#COPY --from=builder /open5gs/install/usr/lib /lib
COPY --from=builder /open5gs/build/configs/open5gs /etc/open5gs 
COPY --from=builder /open5gs/build/configs/freeDiameter /etc/freeDiameter 
COPY --from=builder /open5gs/build/configs/*.yaml /etc/
COPY --from=builder /open5gs/misc/netconf.sh /bin/ 
COPY --from=builder /open5gs/build/tests /bin/tests
COPY --from=builder /my5G-RANTester/cmd/app /bin/rantester
COPY etc /etc
