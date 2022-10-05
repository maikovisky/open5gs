terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.33.0"
    }
    kubernetes = {
      source  = "hashicorp/helm"
      version = "2.5.1"
      source  = "hashicorp/kubernetes"
      version = ">= 2.10.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = "= 1.14.0"
    }
  }
}