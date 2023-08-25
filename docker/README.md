# Docker principal com todos os componentes 

```
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/open5gs-all .
```

# Docker somente com Open5GS

```
cd open5gs
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/open5gs:main -t maikovisky/open5gs:latest -t maikovisky/open5gs:2.6.4 .
```

Comando para gerar imagem para todas as arquiteturas:

```
cd open5gs
sudo docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v6,linux/arm/v7 --push -t maikovisky/open5gs:main  -t maikovisky/open5gs:latest -t maikovisky/open5gs:2.6.4 .
```

# Docker open5gs-ubuntu

```
cd open5gs-ubuntu
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/open5gs-ubuntu:latest -t maikovisky/open5gs-ubuntu:2.6.4 .
```

# Docker WEBUI

```
cd webui
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/webui .
```

# Docker UERANSIM

```
cd ueransim
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/ueransim:3.2.6 .
```


# Docker UPF

```
cd open5gs-upf
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/open5gs-upf:latest -t maikovisky/open5gs-upf:2.6.4 .
```

# Docker IPERF
```
cd iperf
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/iperf:latest
```