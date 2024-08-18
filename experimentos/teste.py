# import json, requests, time
# from pymongo import MongoClient
# from datetime import datetime, timezone
from kubernetes import client, config
# import inspect, signal, getopt, sys, os
# from graphs import GraphanaGetRenderImage
# from experiments import Open5gsSliceExperiment
import k8stools
# from pymongo import MongoClient
# import json
# import os
# import psutil
# import socket
# import struct
# import random
# from pydantic import TypeAdapter, ValidationError
# config.load_kube_config()
# setEnv("open5gs","open5gs-upf-1", "WITH_NICE")
# setEnv("open5gs","open5gs-upf-2", "WITH_NICE")
# setEnv("open5gs","open5gs-upf-3", "WITH_NICE")
# setEnv("open5gs","open5gs-upf-4", "WITH_NICE")
# setEnv("open5gs","open5gs-upf-5", "WITH_NICE")


# IMSI=999700000000000
# SLICE=1
# def get_ipv4_from_nic(interface):
#         interface_addrs = psutil.net_if_addrs().get(interface) or []
#         for snicaddr in interface_addrs:
#             if snicaddr.family == socket.AF_INET:
#                 return snicaddr.address

# def ip2int(addr):
#     return struct.unpack("!I", socket.inet_aton(addr))[0]
        

# addr = get_ipv4_from_nic("eth0")
# IMSI = str(int(IMSI) + ip2int(addr))
# lastOctect = addr.split(".")[-1]
# UEAddr = "10.{}.0.{}".format(40 + int(slice), ip)
# print(UEAddr)

config.load_kube_config()
apps_v1_api = client.CoreV1Api()
# def bandwith(namespace, deployment_name, value = None):
#     apps_v1_api = client.AppsV1Api()
#     annotations = [{
#             'op': "remove" if value == None else "add",  # You can try different operations like 'replace', 'add' and 'remove'
#             'path': '/metadata/annotations',
#             'value': {'kubernetes.io/egress-bandwidth': value}
#         }]
    
#     apps_v1_api.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=annotations)


k8stools.bandwith("open5gs", "open5gs-upf-1", "15M")

#r = apps_v1_api.list_namespaced_pod(namespace="open5gs", label_selector="app=open5gs-upf-1")
#print(r.items[0].metadata.name)



        