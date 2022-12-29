FROM alpine:latest as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
RUN apk update && \
    apk add --no-cache \
       bash \
       iproute2 \
       curl \
       talloc \
       ca-certificates \
       nghttp2-libs \
       libcurl \
       yaml \
       lksctp-tools \
       libmicrohttpd \
       gdb \
       libidn \
       openrc \
       prometheus-node-exporter \
       mongo-c-driver 
    

FROM base as builder
RUN apk add --no-cache \
        alpine-sdk \
        bison \
        flex \
        git \
        cmake \
        meson \
        bash \
        linux-headers \
        bsd-compat-headers \
        yaml-dev \
        lksctp-tools-dev \
        gnutls-dev \
        libgcrypt-dev \
        libidn-dev \
        mongo-c-driver-dev \
        libmicrohttpd-dev \
        curl-dev \
        nghttp2-dev \
        talloc-dev \
        iproute2 && \
        git clone --recursive https://github.com/open5gs/open5gs && \
        cd open5gs && \
	git checkout main  && \
        meson build --prefix=/ && \
#	meson configure -Dmetrics_impl=prometheus build && \
        ninja -C  build && \
        cd build && \
        DESTDIR=/open5gs/install ninja install 

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
COPY --from=builder /open5gs/install/usr/lib /lib
COPY --from=builder /open5gs/build/configs/open5gs /etc/open5gs 
COPY --from=builder /open5gs/build/configs/freeDiameter /etc/freeDiameter 
COPY --from=builder /open5gs/build/configs/*.yaml /etc/
COPY --from=builder /open5gs/misc/netconf.sh /bin/ 
COPY etc /etc



