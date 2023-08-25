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


## Change context

```
kubectl config get-contexts
kubectl config use-context kubernetes-admin@kubernetes  
```