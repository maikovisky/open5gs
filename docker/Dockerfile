FROM alpine:latest as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
RUN apk update && \
    apk add --no-cache \
       bash \
       iproute2 \
       talloc \
       ca-certificates \
       nghttp2-libs \
       libcurl \
       yaml \
       lksctp-tools \
       libmicrohttpd \
       libidn \
       mongo-c-driver 
    

FROM base as builder
RUN apk add --no-cache \
        alpine-sdk \
        bison \
        flex \
        git \
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
    cd open5gs && meson build --prefix=/ && ninja -C build && cd build && DESTDIR=/open5gs/install ninja install 

WORKDIR /


FROM base as final
RUN mkdir -p /var/log/open5gs
WORKDIR /
COPY --from=builder /open5gs/install/bin  /bin 
COPY --from=builder /open5gs/install/lib  /lib
COPY --from=builder /open5gs/build/configs/open5gs /etc/open5gs 
COPY --from=builder /open5gs/build/configs/freeDiameter /etc/freeDiameter 
COPY --from=builder /open5gs/build/configs/*.yaml /etc/




