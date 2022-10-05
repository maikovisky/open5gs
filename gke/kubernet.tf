resource "google_container_cluster" "gke_cluster" {
   # Replace with your Project ID, https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifying_projects
  project  = "${local.gcp_project}"
  location = "${local.gcp_region}"

  name     = "${var.gke_name}"

  #min_master_version = "1.16"

  # Enable Alias IPs to allow Windows Server networking.
  #ip_allocation_policy {
  #  cluster_ipv4_cidr_block  = "/14"
  # services_ipv4_cidr_block = "/20"
  #}

  # Removes the implicit default node pool, recommended when using
  # google_container_node_pool.
  remove_default_node_pool = true
  initial_node_count = "${var.k8s_num_nodes}"
  network = google_compute_network.vpc_main.name
  subnetwork = google_compute_subnetwork.subnet.name

  #
  master_auth {   
    client_certificate_config {
      issue_client_certificate = false
    }
  }

  # node_config {
  #    labels = {
  #       app = "${var.app_name}"
  #   }
  #   tags = ["app", "${var.app_name}"]
  # }
  
  timeouts {
    create = "30m"
    update = "40m"
  }

} 

# Node Pool Gerenciado Separadamente
resource "google_container_node_pool" "gke_node_01" {
  name       = "${google_container_cluster.gke_cluster.name}-node-pool"
  location   = "${local.gcp_region}"
  cluster    = google_container_cluster.gke_cluster.name
  node_count = "${var.k8s_num_nodes}"

  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]

    labels = {
      env = sensitive("${local.gcp_project}")
    }

    machine_type = "e2-standard-2"
    tags         = ["gke-node", sensitive("${local.gcp_project}-gke")]
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}

# Get the credentials 
# resource "null_resource" "get-credentials" {

#  depends_on = [google_container_cluster.sophie_cluster] 
 
#  provisioner "local-exec" {
#    command = "gcloud container clusters get-credentials ${google_container_cluster.sophie_cluster.name} --region=${var.gcp_region}"
#  }
# }

# Create a namespace
# resource "kubernetes_namespace" "monitoring" {
#   #depends_on = [null_resource.get-credentials]
#   metadata {
#     name = "monitoring"
#   }
# }
