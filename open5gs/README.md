# Open5GS

[**Open5GS**](https://open5gs.org/open5gs/docs/) is a C-language Open Source implementation of 5GC and EPC, i.e. the core network of NR/LTE network.


## Prerequisites:

To effectively utilize this repository and its contents related to the 5G core project, the following requirements should be met:

- [**Terraform**](https://www.terraform.io/)
- [**kubectl**](https://kubernetes.io/docs/tasks/tools/)

## Deploy Open5Gs

```
$ terraform apply -auto-approve
```

## Open5GS Applications

### AMF
### AUSF
### BSF
### NRF
### NSSF
### PCF
### SCP
### SMF
### UDM
### UDR
### UPF
### Webui

## UERANSIM Applications

[**UERANSIM**](https://github.com/aligungr/UERANSIM) (pronounced "ju-i ræn sɪm"), is the open source state-of-the-art 5G UE and RAN (gNodeB) simulator. UE and RAN can be considered as a 5G mobile phone and a base station in basic terms. The project can be used for testing 5G Core Network and studying 5G System.

[**UERANSIM**](https://github.com/aligungr/UERANSIM)  introduces the world's first and only open source 5G-SA UE and gNodeB implementation.

The [**UERANSIM**](https://github.com/aligungr/UERANSIM) is used to perform tests on the 5G core control plane, as well as data plane tests, using slices.

### gNB

### UE