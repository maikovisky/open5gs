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
       mongo-c-driver \ 
       nodejs \
       npm
    

FROM base as builder
RUN apk add --no-cache \
        alpine-sdk \
        git \
        meson \
        bash \
        mongo-c-driver-dev \
        libmicrohttpd-dev \
        curl-dev \
        nghttp2-dev \
        talloc-dev \
        iproute2 && \
    git clone --recursive https://github.com/open5gs/open5gs && \
    cd open5gs && cd webui && npm ci --no-optional 

WORKDIR /


FROM base as final
RUN mkdir -p /var/log/open5gs
WORKDIR /webui
ENTRYPOINT ["npm", "run", "dev"]
COPY --from=builder /open5gs/webui /webui
COPY --from=builder /open5gs/misc/netconf.sh /bin/ 



