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
#mongodbUrl = "mongodb+srv://maikovisky:MFIl9m0cgK9UorO9@open5gs.xm3nrzk.mongodb.net/open5gs"
mongodbUrl = "mongodb://localhost:27017/open5gs"

dashboardUID="9ZtOvTcVz"
panelId=62
global osEx


gCorePods = [
    "open5gs-nrf", "open5gs-scp", "open5gs-amf", "open5gs-amf2", "open5gs-ausf","open5gs-bsf", "open5gs-nssf", "open5gs-pcf","open5gs-udm","open5gs-udr", "open5gs-smf"]

gUPFPods = ["open5gs-upf-1", "open5gs-upf-2", "open5gs-upf-3", "open5gs-upf-4", "open5gs-upf-5"]
gURANSIMPods = [] # ["open5gs-ueransim01", "open5gs-ueransim02", "open5gs-ueransim03", "open5gs-ueransim04", "open5gs-ueransim05"]

# gExperiments = json.loads("""[
#     {"experiment": "01", "name": "experiment01", "text": "Baseline only priority UE", "priorityPod": "open5gs-ue01", "pods": [], "slices": ["1"], "cpu": [0], "nice": [0, 0, 0, 0, 0]},                       
#     {"experiment": "02", "name": "experiment02", "text": "Baseline with priority UE and Slice 02", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02"], "slices": ["1","2"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "03", "name": "experiment03", "text": "Baseline with priority UE and Slice 02 and 03", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03"], "slices": ["1","2","3"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "04", "name": "experiment04", "text": "Baseline with priority UE and Slice 02, 03 and 04", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04"], "slices": ["1","2","3","4"], "cpu": [], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "05", "name": "experiment05", "text": "Baseline with priority UE and Slice 02, 03, 04, 05", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "06", "name": "experiment06", "text": "Baseline with priority UE and Slice 02, 03, 04, 05 with nc", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [750, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "07", "name": "experiment07", "text": "Limit CPU all UPF", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [750, 0, 0, 0, 0], "nice": [-5, 0, 0, 0, 0]},
#     {"experiment": "08", "name": "experiment08", "text": "Limit CPU all UPF more Slice 01", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [0, 500, 500, 500, 500], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "09", "name": "experiment09", "text": "Limit CPU all UPF more Slice 02", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 750, 600, 600], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "10", "name": "experiment10", "text": "Limit CPU all UPF more Slice 03", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "11", "name": "experiment11", "text": "Limit CPU all UPF with nice", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525],  "nice": [0, 0, 0, 10, 10]},
#     {"experiment": "12", "name": "experiment12", "text": "Limit CPU all UPF with limit bandwith", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525], "nice": [0, 0, 0, 0, 0], "bandwith": ["12M", "80K", "6M", "20M", "20M"]},
#     {"experiment": "13", "name": "experiment13", "text": "Limit CPU all UPF with nice and limit bandwith", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525], "nice": [0, 0, 0, 10, 10], "bandwith": ["12M", "80K", "6M", "20M", "20M"]},
#     {"experiment": "14", "name": "experiment14", "text": "Baseline with only Slice 04", "priorityPod": "open5gs-ue04", "pods": [], "slices": ["4"], "cpu": [], "nice": [], "bandwith": ["12M", "48K", "3.4M", "21.4M", "21.95M"]}
# ]""")

gExperiments = json.loads("""[
    {"experiment": "01", "name": "experiment01", "text": "Baseline only priority UE", "priorityPod": "open5gs-my5gran01", "pods": [], "slices": ["1"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0], "bandwith": ["-1", "-1", "-1", "-1", "-1"]},                       
    {"experiment": "02", "name": "experiment02", "text": "Baseline with priority UE and Slice 02", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02"], "slices": ["1","2"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0],  "bandwith": ["-1", "-1", "-1", "-1", "-1"]},
    {"experiment": "03", "name": "experiment03", "text": "Baseline with priority UE and Slice 02 and 03", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03"], "slices": ["1","2","3"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0], "bandwith": ["-1", "-1", "-1", "-1", "-1"]},
    {"experiment": "04", "name": "experiment04", "text": "Baseline with priority UE and Slice 02, 03 and 04", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04"], "slices": ["1","2","3","4"], "cpu": [], "nice": [0, 0, 0, 0, 0],"bandwith": ["-1", "-1", "-1", "-1", "-1"]},
    {"experiment": "05", "name": "experiment05", "text": "Baseline with priority UE and Slice 02, 03, 04, 05", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0]},
    {"experiment": "06", "name": "experiment06", "text": "Slice 01, 02, 03, 04, 05 with limit", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 0, 0, 0, 0] ,"nice": [0, 0, 0, 0, 0]},
    {"experiment": "07", "name": "experiment07", "text": "Slice 01, 02, 03, 04, 05 with limit", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 500, 500, 500, 500], "nice": [0, 0, 0, 0, 0]},
    {"experiment": "08", "name": "experiment08", "text": "Slice 01, 02, 03, 04, 05 with limit", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 250, 250, 250, 250], "nice": [0, 0, 0, 0, 0]},
    {"experiment": "09", "name": "experiment09", "text": "Slice 01, 02, 03, 04, 05 with nice", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [0, 0, 0, 0, 0], "limit": [0, 0, 0, 0, 0], "nice": [-5, 0, 0, 0, 0]},
    {"experiment": "10", "name": "experiment10", "text": "Slice 01, 02, 03, 04, 05 with nice", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [0, 0, 0, 0, 0], "limit": [0, 0, 0, 0, 0], "nice": [-5, 5, 5, 5, 5]},
    {"experiment": "11", "name": "experiment11", "text": "Slice 01, 02, 03, 04, 05 with bandwith 0", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["0", "0", "0", "0", "0"], "cpu": [0, 0, 0, 0, 0], "limit": [0, 0, 0, 0, 0],  "nice": [0, 0, 0, 0, 0]},
    {"experiment": "12", "name": "experiment12", "text": "Slice 01, 02, 03, 04, 05 with bandwith 150M", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "150M", "150M", "150M", "150M"], "cpu": [0, 0, 0, 0, 0], "limit": [0, 0, 0, 0, 0],  "nice": [0, 0, 0, 0, 0]},
    {"experiment": "13", "name": "experiment13", "text": "Slice 01, 02, 03, 04, 05 with bandwith 75M", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"],"bandwith": ["-1", "75M", "75M", "75M", "75M"], "cpu": [0, 0, 0, 0, 0], "limit": [0, 0, 0, 0, 0],  "nice": [0, 0, 0, 0, 0]},
    {"experiment": "14", "name": "experiment14", "text": "Experient 06 + 10 - CPU and NICE", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 0, 0, 0, 0] ,"nice": [-5, 5, 5, 5, 5]},
    {"experiment": "15", "name": "experiment15", "text": "Experient 07 + 10 - CPU and NICE", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 500, 500, 500, 500] ,"nice": [-5, 5, 5, 5, 5]},
    {"experiment": "16", "name": "experiment16", "text": "Experient 08 + 10 - CPU and NICE", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "-1", "-1", "-1", "-1"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 250, 250, 250, 250] ,"nice": [-5, 5, 5, 5, 5]},
    {"experiment": "17", "name": "experiment17", "text": "Experient 06 + 11 - CPU and bandwith 0", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["0", "0", "0", "0", "0"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 0, 0, 0, 0] , "nice": [0, 0, 0, 0, 0]},
    {"experiment": "18", "name": "experiment18", "text": "Experient 07 + 11 - CPU and bandwith 0", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["0", "0", "0", "0", "0"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 500, 500, 500, 500], "nice": [0, 0, 0, 0, 0]},
    {"experiment": "19", "name": "experiment19", "text": "Experient 08 + 11 - CPU and bandwith 0", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["0", "0", "0", "0", "0"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 250, 250, 250, 250], "nice": [0, 0, 0, 0, 0]},
    {"experiment": "20", "name": "experiment20", "text": "Experient 06 + 12 - CPU and bandwith 150M", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "150M", "150M", "150M", "150M"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0]},
    {"experiment": "21", "name": "experiment21", "text": "Experient 07 + 12 - CPU and bandwith 150M", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "150M", "150M", "150M", "150M"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 500, 500, 500] ,"nice": [0, 0, 0, 0, 0]},
    {"experiment": "22", "name": "experiment22", "text": "Experient 08 + 12 - CPU and bandwith 150M", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "150M", "150M", "150M", "150M"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 250, 250, 250, 250] ,"nice": [0, 0, 0, 0, 0]},
    {"experiment": "23", "name": "experiment23", "text": "Experient 06 + 10  + 11 - CPU, Nice and bandwith 0", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["0", "0", "0", "0", "0"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 0, 0, 0, 0] ,"nice": [-5, 5, 5, 5, 5]},
    {"experiment": "24", "name": "experiment24", "text": "Experient 06 + 10  + 11 - CPU, Nice and bandwith 150M", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "150M", "150M", "150M", "150M"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 0, 0, 0, 0] ,"nice": [-5, 5, 5, 5, 5]},
    {"experiment": "25", "name": "experiment25", "text": "Experient 07 + 10  + 11 - CPU, Nice and bandwith 0", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["0", "0", "0", "0", "0"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 500, 500, 500] ,"nice": [-5, 5, 5, 5, 5]},
    {"experiment": "26", "name": "experiment26", "text": "Experient 07 + 10  + 11 - CPU, Nice and bandwith 150M", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "bandwith": ["-1", "150M", "150M", "150M", "150M"], "cpu": [1000, 0, 0, 0, 0], "limit": [1000, 500, 500, 500] ,"nice": [-5, 5, 5, 5, 5]}
]""")

# gExperiments = json.loads("""[
#     {"experiment": "01", "name": "experiment01", "text": "Baseline only priority UE", "priorityPod": "open5gs-my5gran01", "pods": [], "slices": ["1"], "cpu": [], "nice": [0, 0, 0, 0, 0]},                     
#     {"experiment": "02", "name": "experiment02", "text": "Baseline with priority UE and Slice 02", "priorityPod": "open5gs-my5gran01", "pods":                ["open5gs-my5gran02"], "slices": ["1","2"], "cpu": [0, 0, 0, 0, 0, 0,0], "nice":  [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "03", "name": "experiment03", "text": "Baseline with priority UE and Slice 02 and 03", "priorityPod": "open5gs-my5gran01", "pods":         ["open5gs-my5gran02", "open5gs-my5gran03"], "slices": ["1","2","3"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "04", "name": "experiment04", "text": "Baseline with priority UE and Slice 02, 03 and 04", "priorityPod": "open5gs-my5gran01", "pods":     ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04"], "slices": ["1","2","3","4"], "cpu": [], "nice": [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "05", "name": "experiment05", "text": "Baseline with priority UE and Slice 02, 03, 04, 05", "priorityPod": "open5gs-my5gran01", "pods":    ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [], "nice":  [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "06", "name": "experiment06", "text": "Baseline with priority UE and Slice 02, 03, 04, 05 ,06", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06"], "slices": ["1","2","3","4","5","6"], "cpu": [], "nice":  [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "07", "name": "experiment07", "text": "Baseline with priority UE and Slice 02, 03, 04, 05, 06, 07", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [], "nice": [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "08", "name": "experiment08", "text": "Baseline with priority UE and Slice 02, 03, 04, 05, 06, 07  with nice", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [], "nice": [0, 0, 0, 5, 10, 10, 10]},
#     {"experiment": "09", "name": "experiment09", "text": "Baseline with priority UE and Slice 02, 03, 04, 05, 06, 07", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [500, 500, 500, 500, 500, 500, 500], "nice": [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "10", "name": "experiment10", "text": "Resource more to 01, 03", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [750, 100, 750, 475, 475, 475, 475], "nice": [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "11", "name": "experiment11", "text": "Resource more to 01", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [930, 100, 750, 430, 430, 430, 430], "nice": [0, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "12", "name": "experiment12", "text": "Baseline with priority UE and Slice 02, 03, 04, 05, 06, 07  with nice", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [0,0,0,0,0,0,0], "nice": [-1, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "13", "name": "experiment13", "text": "Resource more to 01", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [930,100,750, 430, 430, 430, 430], "nice": [-1, 0, 0, 0, 0, 0, 0]},
#     {"experiment": "14", "name": "experiment14", "text": "Resource more to 01", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5","6","7"], "cpu": [1000,400,400, 400, 400, 400, 400], "nice": [0, 0, 0, 0, 0, 0, 0]}

# ]""")
#     {"experiment": "09", "name": "experiment09", "text": "Baseline with priority UE and Slice 02, 03, 04, 05, 06, 07", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","2","3","4","5", "6", "7"], "cpu": [0, 0, 0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0, 0,0]},
#     {"experiment": "10", "name": "experiment10", "text": "Baseline with priority UE and Slice 02, 03, 04, 05 with nc", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [0, 0, 0, 0, 0], "nice": [0, 0, 0, 10, 10]},
#     {"experiment": "11", "name": "experiment11", "text": "Limit CPU all UPF", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [750, 750, 750, 750, 750], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "12", "name": "experiment12", "text": "Limit CPU all UPF more Slice 01", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [900, 750, 750, 675, 675], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "13", "name": "experiment13", "text": "Limit CPU all UPF more Slice 02", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 750, 600, 600], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "14", "name": "experiment14", "text": "Limit CPU all UPF more Slice 03", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525], "nice": [0, 0, 0, 0, 0]},
#     {"experiment": "15", "name": "experiment15", "text": "Limit CPU all UPF with nice", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525],  "nice": [0, 0, 0, 10, 10]},
#     {"experiment": "16", "name": "experiment16", "text": "Limit CPU all UPF with limit bandwith", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525], "nice": [0, 0, 0, 0, 0], "bandwith": ["12M", "80K", "6M", "20M", "20M"]},
#     {"experiment": "17", "name": "experiment17", "text": "Limit CPU all UPF with nice and limit bandwith", "priorityPod": "open5gs-my5gran01", "pods": ["open5gs-my5gran02", "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05"], "slices": ["1","2","3","4","5"], "cpu": [900, 900, 900, 525, 525], "nice": [0, 0, 0, 10, 10], "bandwith": ["12M", "80K", "6M", "20M", "20M"]},
#     {"experiment": "18", "name": "experiment18", "text": "Baseline with only Slice 04", "priorityPod": "open5gs-my5gran04", "pods": [], "slices": ["4"], "cpu": [], "nice": [], "bandwith": ["12M", "48K", "3.4M", "21.4M", "21.95M"]},
#     {"experiment": "19", "name": "experiment19", "text": "Baseline with priority UE and Slice 03, 04, 05, 06, 07", "priorityPod": "open5gs-my5gran01", "pods": [ "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","3","4","5","6","7"], "cpu": [0, 0, 0, 0, 0, 0], "nice": [0, 0, 0, 0, 0, 0]},
#     {"experiment": "20", "name": "experiment20", "text": "Baseline with priority UE and Slice 03, 04, 05, 06, 07", "priorityPod": "open5gs-my5gran01", "pods": [ "open5gs-my5gran03", "open5gs-my5gran04", "open5gs-my5gran05", "open5gs-my5gran06", "open5gs-my5gran07"], "slices": ["1","3","4","5","6","7"], "cpu": [0, 0, 0, 0, 0, 0], "nice": [0, 0, 0, 10, 10, 15]}
# ]""")


gQueries = json.loads("""[
    {"name": "receive", "q": "(sum(irate(container_network_receive_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[30s]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "transmit", "q": "(sum(irate(container_network_transmit_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[30s]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "latency", "q": "sort_desc(avg(irate(ping_average_response_ms{namespace='open5gs', service=~'open5gs-ue01|open5gs-ue02|open5gs-ue03|open5gs-ue04|open5gs-ue05'}[20m:30s])) by(url, job))"},
    {"name": "cpu", "q": "sort_desc(sum(irate(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace='open5gs'}[20m:30s]) * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs' }) by (workload))"},
    {"name": "memory", "q": "sum by(service) (process_resident_memory_bytes{namespace='open5gs'})"},
    {"name": "receive2", "q": "sort_desc(sum(irate(container_network_receive_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[20m:30s]) * on (namespace, pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "transmit2", "q": "sort_desc(sum(irate(container_network_transmit_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[20m:30s]) * on (namespace, pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "receive_packets","q": "sort_desc(sum(irate(container_network_receive_packets_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[20m:30s]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (pod))"},
    {"name": "transmit_packets","q": "sort_desc(sum(irate(container_network_transmit_packets_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[20m:30s]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (pod))"},
    {"name": "received_packets_drop", "q": "sort_desc(sum(irate(container_network_receive_packets_dropped_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[20m:30s]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "transmit_packets_drop", "q": "sort_desc(sum(irate(container_network_transmit_packets_dropped_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[20m:30s]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"}
 ]""")


argumentList = sys.argv[1:]
options = "he:r:t:"
long_options = ["Help", "experiment", "repeat", "time", "core"]
aRepeat = 1
aExp = None
aTime = 240
aTimeBetweenExperience = 60
aCore = False

def usage():
    print("python runExp.py <options>")
    print("<options>:")
    print("\t-e <list>   --experiment <int> Run a list experiment ex. 1,2,3. Default run all")
    print("\t-h          --help             Print this help")
    print("\t-r <int>    --repeat <int>     Repeat the experiments. Default: 1")
    print("\t-t <int>    --time <int>       Time in seconds for each phase to rotate. Default: 300")
    print("\t-c          --core             Change core only")


def search_experiments(experiments, exp):
    for keyval in experiments:
        if exp.lower() == keyval['experiment'].lower():
            return keyval


def run(osEx, r):
    global queries
    print(r)
    osEx.setValues(r)
    osEx.resetCore(wait=True)
    osEx.setPods(r["priorityPod"],r["pods"])
    osEx.start(r)
    osEx.saveInfos(gQueries)
    


try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
except getopt.error as err:    
    # output error, and return with an error code
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    
# checking each argument
for currentArgument, currentValue in arguments:

    if currentArgument in ("-h", "--Help"):
        usage()
        sys.exit()
    elif currentArgument in ("-c", "--core"):
        aCoreOnly = True
        print("Run only core")
    elif currentArgument in ("-e", "--experiment"):
        aExp = currentValue.split(",")
        print (("Run experiment % s") % (aExp))   
    
    elif currentArgument in ("-r", "--repeat"):
        aRepeat = int (currentValue)
        
    elif currentArgument in ("-t", "--time"):
        aTime = int (currentValue)
        
    else:
        assert False, "unhandled option"
        

config.load_kube_config()


print("********                AVISO                ********")
print("* Verificar IPs dos testes de latências dos slices. *")
print("* Verificar IP do ping da UE02.                     *")
print("*****************************************************")


try:
    osEx = Open5gsSliceExperiment(grafanaUrl, prometheusUrl,  mongodbUrl, dashboardUID)
    osEx.setCorePods(gCorePods, gUPFPods, gURANSIMPods)
    osEx.setTime(aTime)
    #osEx.setDebug(True)

    
    for i in range(0, aRepeat):
        print("Cicle {}".format(i + 1))
        
        if(aExp != None):
            for e in aExp:            
                r = search_experiments(gExperiments, e.rjust(2, "0"))
                run(osEx, r)
                time.sleep(aTimeBetweenExperience)
        else:
            for r in gExperiments:
                run(osEx, r)
                time.sleep(aTimeBetweenExperience)
except ConnectionError:
    osEx.stopPods()
    
except KeyboardInterrupt:
    osEx.stopPods()
    sys.stderr.write('\nInterrupted')
