# UERAMSIM

[**UERANSIM**](https://github.com/aligungr/UERANSIM) (pronounced "ju-i ræn sɪm"), is the open source state-of-the-art 5G UE and RAN (gNodeB) simulator. UE and RAN can be considered as a 5G mobile phone and a base station in basic terms. The project can be used for testing 5G Core Network and studying 5G System.

[**UERANSIM**](https://github.com/aligungr/UERANSIM)  introduces the world's first and only open source 5G-SA UE and gNodeB implementation.


## GNode-B


### Files
Files used to deploy the gNB in a Kubernetes cluster.

- gnb.yaml                # Kubernet descriptor
- gnb-init.yaml           # Script init
- gnb-configmap.yaml      # Configmap with nr-gnb config

## UE

### Files
Files used to deploy the UE in a Kubernetes cluster.

- [ue.yaml]
- [ue-init.yaml]
  - [ueinit]:                
  - [initUE.py]:
- [ue-testing.yaml]