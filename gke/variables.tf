# variable "project_id" {
#   description = "GCP Project"
#   type        = string
#   default = ""
# }


locals  {
  gcp_project = "maiko-359801"
  gcp_region  = "us-central1"
}


# variable "gcp_project" {
#   description = "Enter GCP Project"
#   type        = string
#   default     = "maiko-359801"
# }

variable "availability_region_names" {
  description = "Enter GKE cluster region"
  type    = list(string)
  default = ["us-central1", "southamerica-east1"]
}


variable "gke_name" {
  type = string
  description = "Enter GKE cluster name"
}

# variable "gke_username" {
#   type    = string
#   description = "GKE cluster username"
# }

# variable "gke_password" {
#   type    = string
#   description = "GKE cluster password" 
# }

variable "k8s_num_nodes" {
  description = "GKE cluster number of nodes"
  type        = number
  default     = 1
}

