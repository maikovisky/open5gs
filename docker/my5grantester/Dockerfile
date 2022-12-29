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
       prometheus-node-exporter 
    

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
        libmicrohttpd-dev \
        curl-dev \
        nghttp2-dev \
        talloc-dev \
        go \
        iproute2 && \
#        git clone https://github.com/my5G/my5G-RANTester.git && \
	git clone https://github.com/gabriel-lando/my5G-RANTester.git && \
        cd my5G-RANTester && \
	go mod download && \
	cd cmd && \
	go build app.go 

WORKDIR /


FROM base as final
RUN mkdir -p /my5G-RANTester/config

WORKDIR /my5G-RANTester/cmd
COPY --from=builder /my5G-RANTester/cmd  /my5G-RANTester/cmd
COPY etc /etc



