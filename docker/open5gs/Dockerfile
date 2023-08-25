FROM alpine:3.16.5 as base-3.16.5
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
    

FROM base-3.16.5 as builder
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
        meson build --prefix=/ && \
        ninja -C  build && \
        cd build && \
        DESTDIR=/open5gs/install ninja install 

WORKDIR /

FROM base-3.16.5 as final
RUN mkdir -p /var/log/open5gs \
    rc-update add node-exporter default

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



