
# Create Virtual Private Cloud
resource "google_compute_network" "vpc_main" {
  name        = "vpc-main"
  project     = "${local.gcp_project}"

  auto_create_subnetworks = false
  mtu                     = 1460
  routing_mode            = "REGIONAL"
}


# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "dev-sophie-subnet"
  region        = "${local.gcp_region}"
  network       = google_compute_network.vpc_main.id
  ip_cidr_range = "10.10.0.0/24"
  private_ip_google_access = true

  #secondary_ip_range = {
  #  ip_cidr_range = "k8s-pod-ranger"
  #  range_name = "10.48.0.0/14"
  #} 

  #secondary_ip_range = {
  #  ip_cidr_range = "k8s-service-ranger"
  #  range_name = "10.52.0.0/20"
  #}
}

# Subnet
# resource "google_compute_subnetwork" "qa_subnet" {
#   name          = "qa-sophie-subnet"
#   region        = "${var.gcp_region}"
#   network       = google_compute_network.vpc_network.name
#   ip_cidr_range = "10.11.0.0/24"

#   count         = var.qa ? 1 : 0
# }

# # Subnet
# resource "google_compute_subnetwork" "prod_subnet" {
#   name          = "prod-sophie-subnet"
#   region        = "${var.gcp_region}"
#   network       = google_compute_network.vpc_network.name
#   ip_cidr_range = "10.12.0.0/24"

#   count         = var.prod ? 1 : 0
# }

# Exemplo video
#resource "google_compute_router" "dev_router" {
#  name = "dev_router"
#  region = "${var.gcp_region}"
#  network = google_compute_network.vpc_network.id 
#}

#resource "google_compute_router_nat" "dev_nat" {
#  name = "dev_nat"
#  router = google_compute_router.dev_router.id
#  region = "${var.gcp_region}"
#  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
#  nat_ip_allocate_option = "MANUAL_ONLY"

#  subnetwork {
#    name = google_compute_subnetwork.dev_subnet.id
#    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
#  }

#  nat_ips = [google_compute_address.nat.self_link]
#}

#resource "google_compute_address" "dev_nat" {
#  name = "dev_nat"
#  address_type = "EXTERNAL"
#  network_tier = "PREMIUM"
#
#  depends_on = [
#    google_project_service.compute
#  ] 
#}