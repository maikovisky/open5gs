# output "region" {
#   value       = "${var.region}"
#   description = "Região do GCloud"
# }

output "gcp_project" {
  description = "ID do projeto GCP"
  #sensitive   = true
  value       = "${local.gcp_project}"
}

output "gke_name" {
  description = "GKE string connection"
  value       = "${var.gke_name}"
}

# output "kubernetes_cluster_name" {
#   value       = google_container_cluster.sophie_cluster.name
#   description = "Nome do cluster GKE"
#   sensitive   = true
# }

# output "kubernetes_cluster_host" {
#   value       = google_container_cluster.sophie_cluster.endpoint
#   description = "Host do cluster GKE"
#   sensitive   = true
# }