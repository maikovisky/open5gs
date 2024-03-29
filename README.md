# Mestrado

This repository houses the tools and applications developed during the 5G-focused master's program. Within this repository, you'll discover the configurations employed by Open5gs within a Kubernetes cluster, along with Dockerfiles for generating the application images. Additionally, there are other details provided for the deployment of a 5G core.

## Open5gs

Open5GS is a C-language Open Source implementation of 5GC and EPC, i.e. the core network of NR/LTE network.

### Imagens 

These are the images employed in the project, all based on Ubuntu and each with its own unique characteristics. Further information about the images can be found in the [Docker](docker/README.md) folder.

- [**maikovisky/open5gs:2.6.4**](https://hub.docker.com/repository/docker/maikovisky/open5gs): Use in AMF, AUSF, BSF, NSSF, PCF, SCP, SMF, UDM, UDR
- [**maikovisky/open5gs-upf:2.6.4**](https://hub.docker.com/repository/docker/maikovisky/open5gs-upf): Use in UPF
- [**maikovisky/open5gs-webui:latest**](https://hub.docker.com/repository/docker/maikovisky/open5gs-webui): Use in Webui
- [**maikovisky/ueransim:3.2.6**](https://hub.docker.com/repository/docker/maikovisky/ueransim): Use in gNB, UE 


# Docker

```
cd docker
docker build -t maikovisky/openg5s .

```

## Multiplataform

Install QEMU  

```
sudo apt install -y qemu-user-static binfmt-support
```

Create image

```
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v6,linux/arm/v7  -o type=docker -t maikovisky/open5gs .
```
 
 OR

```
docker buildx build --platform linux/amd64 --push -t maikovisky/open5gs:2.5.5 -t maikovisky/open5gs:latest .
```

## Wireshark (sniffer)

### Install

Need [insall krew](https://krew.sigs.k8s.io/docs/) and after plugin sniff 

```
krew install krew
kubectl krew install sniff
```


### Capture packets in wireshark

```
kubectl sniff <pod>
```


## Troubleshooting

- [UPF and SMF core dump](https://github.com/open5gs/open5gs/issues/1911)

### Problema de Roteamento entre UE e o UPF. 

Um problema que esta sendo enfrentado é permitir com que UE consiga acessar algum conteúdo na Internet. Para isso é necessário que o UE faça a conexção com o UPF, onde irá receber um IP e criar um tunel entre os dois. A baixo a topologia:

!(/imagens/open5gs-UE-UPF.png)


#### Status
```
[ OK] eth0 (upf) => Internet
[ OK] uesimtun0  => ogstun
[NOK] uesimtun0  => eth0 (upf)
[NOK] ogstun     => eth0 (upf)
[NOK] ogstun     => Internet
```

#### Solução sugerida

Na máquina UPF configurar o TUN.

```
ip tuntap add name ogstun mode tun
ip addr add 192.168.0.1/16 dev ogstun
ip addr add 2001:db8:cafe::1/48 dev ogstun
ip link set ogstun up
```

Permitir o encaminhamento entre as interfaces
```
### Enable IPv4/IPv6 Forwarding
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1

### Add NAT Rule
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

#### Testando

Rodar os comandos abaixo no POD UERAMSIM enquanto captura o trafego de rede usando o comando kubectl sniff <UPF_POD_ID>

```
ping -I uesimtun0 8.8.8.8
iperf -B 192.168.0.2 -c open5gs-iperf -w 300k
iperf -B 192.168.0.2 -c open5gs-iperf -w 300k -u
iperf -B 192.168.0.2 -c open5gs-iperf -w 300k -r
iperf -B 192.168.0.2 -c open5gs-iperf -w 300k -r -u

iperf -B 10.41.0.13 -c open5gs-iperf -t 60 -i 5 --trip-times --txstart-time $(expr $(date +%s) + 1).$(date+%N)
```

```
kubectl cp <POD_ID>:/var/tcpdump .
```

#### Algumas discuções sobre o assunto
- [Promissor](https://unix.stackexchange.com/questions/442760/cant-forward-traffic-from-eth-to-tun-tap)
- [Base do trabalho do Grabriel](https://github.com/my5G/my5G-RANTester/wiki/Tutorial-open5GS-v2.3.6)


### [error] Initial Registration failed [UE_IDENTITY_CANNOT_BE_DERIVED_FROM_NETWORK]

UERANSIM não esta conseguindo conectar. 

## Links
- (https://brito.com.br/posts/build-docker-arm64/)
- (https://bitbucket.org/infinitydon/workspace/projects/PROJ)
- (https://bitbucket.org/infinitydon/opensource-5g-core-service-mesh/src/main/)
- (https://medium.com/@googler_ram/100-opensource-5g-projects-that-you-can-get-your-hands-dirty-with-127a50967692)
- (https://open5gs.org/open5gs/docs/platform/08-alpine/)
- (https://github.com/my5G/my5G-RANTester)
- (https://github.com/PORVIR-5G-Project/my5G-RANTester)
- (https://github.com/aligungr/UERANSIM)
- (https://github.com/s5uishida/open5gs_5gc_ueransim_sample_config#overview)