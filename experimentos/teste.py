import json, requests, time
from pymongo import MongoClient
from datetime import datetime, timezone
from kubernetes import client, config
import inspect, signal, getopt, sys, os
from graphs import GraphanaGetRenderImage
from experiments import Open5gsSliceExperiment



grafanaUrl = "http://maikovisky:SuperSenha2024@localhost:3000"
prometheusUrl = "http://localhost:9090"
#mongodbUrl = "mongodb://localhost:27020/open5gs"
mongodbUrl = "mongodb+srv://maikovisky:MFIl9m0cgK9UorO9@open5gs.xm3nrzk.mongodb.net/open5gs"
dashboardUID="9ZtOvTcVz"

mongodbUrl = "mongodb+srv://maikovisky:MFIl9m0cgK9UorO9@open5gs.xm3nrzk.mongodb.net/open5gs"
conn = MongoClient(mongodbUrl)
db = conn["open5gs"]

coll = db["experiments"]


gri = GraphanaGetRenderImage(grafanaUrl, dashboardUID)
cursor  = coll.find({"experiment": "01"})
for c in cursor:
    startAt, endAt = [c["fases"][0] * 1000, c["fases"][-1]]
    slices = [str(int(x)) for x in c["slices"]]
    name  = "experiment{}".format(c["experiment"])
    print(slices)
    aText = "(Experiment {} - {})".format(c["experiment"], c["number"])
    print("From {}  To {}".format(startAt, endAt))
    gri.downloadImages(startAt, endAt, name, aText, slices, c["number"])
        
    

    





        