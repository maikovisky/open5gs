# Mestrado

# Terraform para GKE

```
$env:GOOGLE_PROJECT="maiko-359801"
$env:GOOGLE_REGION="us-central1"
$env:KUBE_CONFIG_PATH="~/.kube/config" 
gcloud config set project $env:GOOGLE_PROJECT
cd gke
terraform init
terraform apply -parallelism=n
gcloud container clusters get-credentials gke-slice --region $env:GOOGLE_REGION --project $env:GOOGLE_PROJECT
```

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


# Links
- https://brito.com.br/posts/build-docker-arm64/
- https://bitbucket.org/infinitydon/workspace/projects/PROJ
- https://bitbucket.org/infinitydon/opensource-5g-core-service-mesh/src/main/
- https://medium.com/@googler_ram/100-opensource-5g-projects-that-you-can-get-your-hands-dirty-with-127a50967692
- https://open5gs.org/open5gs/docs/platform/08-alpine/
- https://github.com/my5G/my5G-RANTester
- https://github.com/PORVIR-5G-Project/my5G-RANTester
- https://github.com/aligungr/UERANSIM
- https://github.com/s5uishida/open5gs_5gc_ueransim_sample_config#overview