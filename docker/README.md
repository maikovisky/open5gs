# Docker principal com todos os componentes 

```
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/open5gs-all .
```

# Docker somente com Open5GS
```
cd open5gs
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/open5gs .
```

Comando para gerar imagem para todas as arquiteturas:

```
cd open5gs
sudo docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v6,linux/arm/v7 --push -t maikovisky/open5gs .
```

# Docker WEBUI

```
cd webui
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/webui .
```

# Docker UERANSIM

```
cd ueransim
sudo docker buildx build --platform linux/amd64 --push -t maikovisky/ueransim .
```