# Criando namesapce open5gs
resource "kubernetes_namespace" "open5gs" {
   metadata {
     name = "open5gs"
   }
}


# MongoDB
data "kubectl_path_documents" "mongodb_manifests" {
    pattern = "./mongodb/*.yaml"
}

resource "kubectl_manifest" "mongodb" {
    count     = length(data.kubectl_path_documents.mongodb_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.mongodb_manifests.documents, count.index)
}

# AMF Database
data "kubectl_path_documents" "amf_manifests" {
    pattern = "./amf/*.yaml"
}

resource "kubectl_manifest" "amf" {
    count     = length(data.kubectl_path_documents.amf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.amf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# NRF Database
data "kubectl_path_documents" "nrf_manifests" {
    pattern = "./nrf/*.yaml"
}

resource "kubectl_manifest" "nrf" {
    count     = length(data.kubectl_path_documents.nrf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.nrf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.mongodb_manifests
    ]
}


