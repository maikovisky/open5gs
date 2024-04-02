import json
import requests
from datetime import datetime, timezone
from kubernetes import client, config



#PROMETHEUS="http://localhost:55061"

#query='(sum(irate(container_network_receive_bytes_total{job="kubelet",namespace='open5gs'}[1m])* on (namespace,pod) group_left(workload) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))'
#query='container_network_receive_bytes_total{job="kubelet",namespace='open5gs'}  on (namespace,pod)'

#txt = requests.get(PROMETHEUS+'/api/v1/query_range?start=2024-03-21T04:33:44.000Z&end=2024-03-21T04:53:44.000Z&step=5s&query='+query).text
#print(txt)
#j = json.loads(txt)
#print(j['data'])

grafanaUrl="http://admin:admin@localhost:3000"
prometheusUrl=""
dashboardUID="9ZtOvTcVz"
panelID=69

 
 # t=$(date +%s%N | cut -b1-13)
 # curl --location 'http://admin:admin@10.107.242.246/api/annotations'  --header 'Accept: application/json'  --header 'Content-Type: application/json' --data "{ \"dashboardUID\": \"9ZtOvTcVz\", \"panelId\": 54, \"time\":$t, \"text\": \"$varText\", \"tags\": [\"open5gs\"]}"




# config.load_kube_config()
# v1 = client.CoreV1Api()
# print("Listing pods with their IPs:")
# pod_list = v1.list_namespaced_pod("open5gs")
# x = pod_list
# for pod in pod_list.items:
#     #if(pod.metadata.name.startswith("open5gs-ue01") and pod.status.phase == "Running"):
        
#     print("%s\t%s\t%s" % (pod.metadata.name,
#                         pod.status.phase,
#                         pod.status.pod_ip))


# e = """[
#     {"experiment": "01", "text": "Baseline only priority UE", "priorityPod": "open5gs-ue01", "pods": []},                       
#     {"experiment": "02", "text": "Baseline with priority UE and Slice 02", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02"]},
#     {"experiment": "03", "text": "Baseline with priority UE and Slice 02 and 03", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03"]},
#     {"experiment": "04", "text": "Baseline with priority UE and Slice 02, 03 and 04", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04"]},
#     {"experiment": "05", "text": "Baseline with priority UE and Slice 02, 03, 04, 05", "priorityPod": "open5gs-ue01", "pods": ["open5gs-ue02", "open5gs-ue03", "open5gs-ue04", "open5gs-ue05"]}
#     ]"""

# experiments = json.loads(e)

# print(experiments)

# def search_experiments(experiments, exp):
#     for keyval in experiments:
#         if exp.lower() == keyval['experiment'].lower():
#             return keyval

# exp = search_experiments(experiments, "02")
# print(exp["experiment"])


queries = json.loads("""[
    {"name": "receive", "q": "(sum(irate(container_network_receive_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[2m]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "transmit", "q": "(sum(irate(container_network_transmit_bytes_total{job='kubelet', metrics_path='/metrics/cadvisor', namespace='open5gs'}[2m]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))"},
    {"name": "latency", "q": "avg by(url, job) (irate(ping_average_response_ms{namespace='open5gs', service=~'open5gs-ue01|open5gs-ue02|open5gs-ue03|open5gs-ue04|open5gs-ue05'}[$_rate_interval]))"},
    {"name": "cpu", "q": "sum(irate(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace='open5gs'}[2m]) * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs' }) by (workload)"},
    {"name": "memory", "q": "sum by(service) (process_resident_memory_bytes{namespace='open5gs'})"}
 ]""")

    # {"name": "transmit", "q": '(sum(irate(container_network_transmit_bytes_total{job="kubelet", metrics_path="/metrics/cadvisor", namespace='open5gs'}[2m]) * on (namespace,pod) group_left(workload,workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs'}) by (workload, interface))'},
    # {"name": "latency", "q": 'avg by(url, job) (irate(ping_average_response_ms{namespace='open5gs', service=~"open5gs-ue01|open5gs-ue02|open5gs-ue03|open5gs-ue04|open5gs-ue05"}[$_rate_interval]))'},
    # {"name": "cpu", "q": 'sum(irate(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace='open5gs'}[2m]) * on(namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace='open5gs' }) by (workload)'},
    # {"name": "memory", "q": 'sum by(service) (process_resident_memory_bytes{namespace='open5gs'})'}

ns = {}
for q in queries:
    metric = q['name']
    query  = q['q']
    start = "2024-03-23T15:00:00.000Z"
    end = "2024-03-23T18:00:00.000Z"
    prometheus = "http://localhost:9090"
    apiEndpoint = "{}/api/v1/query_range?start={}&end={}&step=5s&query={}".format(prometheus, start, end, q['q'])
    #txt = requests.get(apiEndpoint).text
    #print(txt)
    ns[metric] = query

print(ns)
    
    



