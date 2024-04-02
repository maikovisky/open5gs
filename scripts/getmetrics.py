import json, requests
from datetime import datetime, timezone
from kubernetes import client, config



#PROMETHEUS="http://localhost:55061"

#query='(sum(irate(container_network_receive_bytes_total{job="kubelet",namespace="open5gs"}[1m])* on (namespace,pod) group_left(workload) namespace_workload_pod:kube_pod_owner:relabel{namespace="open5gs"}) by (workload, interface))'
#query='container_network_receive_bytes_total{job="kubelet",namespace="open5gs"}  on (namespace,pod)'

#txt = requests.get(PROMETHEUS+'/api/v1/query_range?start=2024-03-16T20:31:19.000Z&end=2024-03-16T20:59:19.000Z&step=5s&query='+query).text
#print(txt)
#j = json.loads(txt)
#print(j['data'])

grafanaUrl="http://admin:admin@localhost:3000"
prometheusUrl=""
dashboardUID="9ZtOvTcVz"
panelID=69

 
 # t=$(date +%s%N | cut -b1-13)
 # curl --location 'http://admin:admin@10.107.242.246/api/annotations'  --header 'Accept: application/json'  --header 'Content-Type: application/json' --data "{ \"dashboardUID\": \"9ZtOvTcVz\", \"panelId\": 54, \"time\":$t, \"text\": \"$varText\", \"tags\": [\"open5gs\"]}"



def setAnnotation(text, dashboardUID="9ZtOvTcVz",panelId=69):
    global grafanaUrl
    timeStart = int(datetime.now(timezone.utc).timestamp() * 1000)
    url=grafanaUrl + "/api/annotations"
    header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    body = { "dashboardUID": dashboardUID, "panelId": panelId, "time": timeStart, "text": text, "tags": ["open5gs"]}
    print(body)
    r = requests.post(url, headers=header, data=json.dumps(body))
    print(r.content)
    return timeStart

def start():
    print("Start")
    setAnnotation("Start")
    return True

def do():
    return True

def stop(): 
    return True


config.load_kube_config()
v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
pod_list = v1.list_namespaced_pod("open5gs")
x = pod_list
for pod in pod_list.items:
    if(pod.metadata.name.startswith("open5gs-ue01") and pod.status.phase == "Running"):
        
        print("%s\t%s\t%s" % (pod.metadata.name,
                            pod.status.phase,
                            pod.status.pod_ip))
# k8sApi = client.AppsV1Api()

#k8sApi.patch_namespaced_deployment_scale(name="open5gs-ue01", namespace="open5gs", body={'spec': {'replicas': 5}})

#start()







