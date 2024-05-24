import json, requests, time
from pymongo import MongoClient
from datetime import datetime, timezone
from kubernetes import client, config
import inspect, signal, getopt, sys, os
from graphs import GraphanaGetRenderImage
from experiments import Open5gsSliceExperiment
from k8stools import *


config.load_kube_config()
setEnv("open5gs","open5gs-upf-1", "WITH_NICE")
setEnv("open5gs","open5gs-upf-2", "WITH_NICE")
setEnv("open5gs","open5gs-upf-3", "WITH_NICE")
setEnv("open5gs","open5gs-upf-4", "WITH_NICE")
setEnv("open5gs","open5gs-upf-5", "WITH_NICE")




    

    





        