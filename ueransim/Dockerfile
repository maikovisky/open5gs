FROM alpine:latest as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
RUN apk update && \
    apk add --no-cache \
       bash \
       libstdc++ \
       iproute2 \
       curl \
       lksctp-tools \
       net-tools  
    

FROM base as builder
RUN apk add --no-cache \
        alpine-sdk \
        gcc \
        g++ \
        linux-headers \
        lksctp-tools-dev \
        cmake \
        iproute2 && \
    git clone --recursive https://github.com/aligungr/UERANSIM && \
    cd UERANSIM && make && chmod a+x build/nr-binder 

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



