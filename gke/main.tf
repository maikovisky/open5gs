# https://www.youtube.com/watch?v=X_IK0GBbBTw

provider "google" {
    credentials = file("credentials/maiko-359801-20c77b2e5d45.json")
    project     = "${local.gcp_project}"
    region      = "${local.gcp_region}"
}
