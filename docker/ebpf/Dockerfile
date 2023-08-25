FROM ubuntu:jammy as base
MAINTAINER Maiko de Andrade <maikovisky@gmail.com>
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y curl \
        gdb \
	cmake \
	clang \
	libelf1 \ 
	libelf-dev \
	zlib1g-dev \
	llvm-dev \
	libpcap-dev \
	libbfd-dev \
	net-tools \
	iproute2 \
	iptables \
	iputils-ping \
	cargo \
	git \
        vim && \
	git clone --recurse-submodules https://github.com/libbpf/libbpf-bootstrap && \
	cd libbpf-bootstrap/examples/c && \
	make && \
	cd ../../../ && \
	git clone https://github.com/libbpf/libbpf-rs.git && \
	cd libbpf-rs && \
	cargo build --release

WORKDIR /

