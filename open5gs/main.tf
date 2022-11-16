# Criando namesapce open5gs
# resource "kubernetes_namespace" "open5gs" {
#    metadata {
#      name = "open5gs"
#    }
# }


# MongoDB
data "kubectl_path_documents" "mongodb_manifests" {
    pattern = "./mongodb/*.yaml"
}

resource "kubectl_manifest" "mongodb" {
    count     = length(data.kubectl_path_documents.mongodb_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.mongodb_manifests.documents, count.index)
}

# freeDiameter
data "kubectl_path_documents" "free_diameter_manifests" {
    pattern = "./freeDiameter/*.yaml"
}

resource "kubectl_manifest" "free_diameter" {
    count     = length(data.kubectl_path_documents.free_diameter_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.free_diameter_manifests.documents, count.index)
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


# SCP Database
data "kubectl_path_documents" "scp_manifests" {
    pattern = "./scp/*.yaml"
}

resource "kubectl_manifest" "scp" {
    count     = length(data.kubectl_path_documents.scp_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.scp_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.mongodb_manifests,
      data.kubectl_path_documents.nrf_manifests
    ]
}

# AMF Database
data "kubectl_path_documents" "amf_manifests" {
    pattern = "./amf/*.yaml"
}

resource "kubectl_manifest" "amf" {
    count     = length(data.kubectl_path_documents.amf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.amf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.scp_manifests
    ]
}

# AUSF Database
data "kubectl_path_documents" "ausf_manifests" {
    pattern = "./ausf/*.yaml"
}

resource "kubectl_manifest" "ausf" {
    count     = length(data.kubectl_path_documents.ausf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.ausf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}


# BSF Database
data "kubectl_path_documents" "bsf_manifests" {
    pattern = "./bsf/*.yaml"
}

resource "kubectl_manifest" "bsf" {
    count     = length(data.kubectl_path_documents.bsf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.bsf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}


# HSS Database
# data "kubectl_path_documents" "hss_manifests" {
#     pattern = "./hss/*.yaml"
# }

# resource "kubectl_manifest" "hss" {
#     count     = length(data.kubectl_path_documents.hss_manifests.documents)
#     yaml_body = element(data.kubectl_path_documents.hss_manifests.documents, count.index)

#     depends_on = [
#       data.kubectl_path_documents.nrf_manifests,
#       resource.kubectl_manifest.free_diameter
#     ]
# }


# MME Database
data "kubectl_path_documents" "mme_manifests" {
    pattern = "./mme/*.yaml"
}

resource "kubectl_manifest" "mme" {
    count     = length(data.kubectl_path_documents.mme_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.mme_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests,
      resource.kubectl_manifest.free_diameter
    ]
}

# NSSF Database
data "kubectl_path_documents" "nssf_manifests" {
    pattern = "./nssf/*.yaml"
}

resource "kubectl_manifest" "nssf" {
    count     = length(data.kubectl_path_documents.nssf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.nssf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# PCRF Database
# data "kubectl_path_documents" "pcrf_manifests" {
#     pattern = "./pcrf/*.yaml"
# }

# resource "kubectl_manifest" "pcrf" {
#     count     = length(data.kubectl_path_documents.pcrf_manifests.documents)
#     yaml_body = element(data.kubectl_path_documents.pcrf_manifests.documents, count.index)

#     depends_on = [
#       data.kubectl_path_documents.nrf_manifests
#     ]
# }

# PCF Database
data "kubectl_path_documents" "pcf_manifests" {
    pattern = "./pcf/*.yaml"
}

resource "kubectl_manifest" "pcf" {
    count     = length(data.kubectl_path_documents.pcf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.pcf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}


# sgwc
data "kubectl_path_documents" "sgwc_manifests" {
    pattern = "./sgwc/*.yaml"
}

resource "kubectl_manifest" "sgwc" {
    count     = length(data.kubectl_path_documents.sgwc_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.sgwc_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# smf
data "kubectl_path_documents" "smf_manifests" {
    pattern = "./smf/*.yaml"
}

resource "kubectl_manifest" "smf" {
    count     = length(data.kubectl_path_documents.smf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.smf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# udm
data "kubectl_path_documents" "udm_manifests" {
    pattern = "./udm/*.yaml"
}

resource "kubectl_manifest" "udm" {
    count     = length(data.kubectl_path_documents.udm_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.udm_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# sgwu
data "kubectl_path_documents" "sgwu_manifests" {
    pattern = "./sgwu/*.yaml"
}

resource "kubectl_manifest" "sgwu" {
    count     = length(data.kubectl_path_documents.sgwu_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.sgwu_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# UDR
data "kubectl_path_documents" "udr_manifests" {
    pattern = "./udr/*.yaml"
}

resource "kubectl_manifest" "udr" {
    count     = length(data.kubectl_path_documents.udr_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.udr_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# UPF
data "kubectl_path_documents" "upf_manifests" {
    pattern = "./upf/*.yaml"
}

resource "kubectl_manifest" "upf" {
    count     = length(data.kubectl_path_documents.upf_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.upf_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# webui
data "kubectl_path_documents" "webui_manifests" {
    pattern = "./webui/*.yaml"
}

resource "kubectl_manifest" "webui" {
    count     = length(data.kubectl_path_documents.webui_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.webui_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}

# POD for teste
#data "kubectl_path_documents" "test_manifests" {
#    pattern = "./test/*.yaml"
#}

#resource "kubectl_manifest" "test" {
#    count     = length(data.kubectl_path_documents.test_manifests.documents)
#    yaml_body = element(data.kubectl_path_documents.test_manifests.documents, count.index)

#    depends_on = [
#      data.kubectl_path_documents.nrf_manifests
#    ]
#}

# POD for ueransim
data "kubectl_path_documents" "ueransim_manifests" {
    pattern = "./ueransim/*.yaml"
}

resource "kubectl_manifest" "ueransim" {
    count     = length(data.kubectl_path_documents.ueransim_manifests.documents)
    yaml_body = element(data.kubectl_path_documents.ueransim_manifests.documents, count.index)

    depends_on = [
      data.kubectl_path_documents.nrf_manifests
    ]
}



