import json, requests, time
from pymongo import MongoClient
from datetime import datetime, timezone
from kubernetes import client, config
import inspect, signal, getopt, sys, os
from graphs import GraphanaGetRenderImage
from experiments import Open5gsSliceExperiment

grafanaUrl = "http://admin:prom-operator@localhost:3000"
prometheusUrl = "http://localhost:9090"
mongodbUrl = "mongodb://localhost:27020/open5gs"
dashboardUID="9ZtOvTcVz"
panelId=62
global osEx



gExperiments = json.loads("""[
    {"experiment": "01", "name": "experiment01", "text": "Baseline only priority UE", "priorityPod": "open5gs-ue01", "pods": [], "slices": ["1"]},                       
    {"experiment": "02", "name": "experiment02", "text": "Baseline with priority UE and Slice 02", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02"], "slices": ["1","2"]},
    {"experiment": "03", "name": "experiment03", "text": "Baseline with priority UE and Slice 02 and 03", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03"], "slices": ["1","2","3"]},
    {"experiment": "04", "name": "experiment04", "text": "Baseline with priority UE and Slice 02, 03 and 04", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04"], "slices": ["1","2","3","4"]},
    {"experiment": "05", "name": "experiment05", "text": "Baseline with priority UE and Slice 02, 03, 04, 05", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"], "slices": ["1","2","3","4","5"]}
]""")


gQueries = json.loads("""[
    {"name": "receive", "q": "(sum(irate(container_network_receive_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[2m]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "transmit", "q": "(sum(irate(container_network_transmit_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[2m]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "latency", "q": "avg by(url, job) (irate(ping_average_response_ms{namespace='open5gs', service=~'open5gs-ue01|open5gs-ue02|open5gs-ue03|open5gs-ue04|open5gs-ue05'}[2m]))"},
    {"name": "cpu", "q": "sum(irate(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace='open5gs'}[2m]) * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs' }) by (workload)"},
    {"name": "memory", "q": "sum by(service) (process_resident_memory_bytes{namespace='open5gs'})"}
 ]""")


argumentList = sys.argv[1:]
options = "he:r:t:"
long_options = ["Help", "experiment", "repeat", "time"]
aRepeat = 1
aExp = None
aTime = 300

def usage():
    print("python runExp.py <options>")
    print("<options>:")
    print("\t-e <list>   --experiment <int> Run a list experiment ex. 1,2,3. Default run all")
    print("\t-h          --help             Print this help")
    print("\t-r <int>    --repeat <int>     Repeat the experiments. Default: 1")
    print("\t-t <int>    --time <int>       Time in seconds for each phase to rotate. Default: 300")


def search_experiments(experiments, exp):
    for keyval in experiments:
        if exp.lower() == keyval['experiment'].lower():
            return keyval


def run(osEx, r):
    global queries
    print(r)
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

try:
    osEx = Open5gsSliceExperiment(grafanaUrl, prometheusUrl,  mongodbUrl, dashboardUID)
    osEx.setTime(aTime)

    
    for i in range(0, aRepeat):
        print("Cicle {}".format(i + 1))
        
        if(aExp != None):
            for e in aExp:            
                r = search_experiments(gExperiments, e.rjust(2, "0"))
                run(osEx, r)
                time.sleep(240)
        else:
            for r in gExperiments:
                run(osEx, r)
                time.sleep(240)
            
except KeyboardInterrupt:
    osEx.stopPods()
    sys.stderr.write('\nInterrupted')
