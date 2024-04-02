import json, requests, time
from pymongo import MongoClient
from datetime import datetime, timezone
from kubernetes import client, config
import os
from graphs import GraphanaGetRenderImage


class Open5gsSliceExperiment:
    
    def __init__(self, grafanaUrl, prometheusUrl, mongodbUrl, dashUID, namespace="open5gs"):
        self.grafanaUrl = grafanaUrl
        self.prometheus = prometheusUrl 
        self.mongodbUrl = mongodbUrl
        self.dashboardUID = dashUID
        self.debug = False

        self.namespace = namespace
        self.tags = ["open5gs"]
        self.priorityPod = "open5gs-ue01"
        self.pods = []
        self.time = 300

        self.gri = GraphanaGetRenderImage(grafanaUrl, dashUID)
        
    def setDebug(self, debug=True):
        self.debug = debug
    
    def setTime(self, time):
        self.time = time
        
    def getDatabase(self, database):
        # DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb://localhost:27020/open5gs")
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        conn = MongoClient(self.mongodbUrl)
        return conn[database]
        
    def addAnnotation(self, text, startAt = False, endAt = False):
        t = datetime.now(timezone.utc)
        
        if(startAt):
            self.startAt = t
            #print(self.startAt.strftime("%Y-%m-%dT%H:%M:%S.000Z"))

        if(endAt):
            self.endAt = t
            
        timeStart = int( t.timestamp() * 1000)
                    
        header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = { "dashboardUID": self.dashboardUID, "time": timeStart, "text": text, "tags": self.tags }

        r = requests.post(self.grafanaUrl + "/api/annotations", headers=header, data=json.dumps(body))
        print(text)
        return int( t.timestamp() )   
    
    def scale(self, pod, replicas):
        k8sApi = client.AppsV1Api()
        k8sApi.patch_namespaced_deployment_scale(name=pod, namespace=self.namespace, body={'spec': {'replicas': replicas}})
        print("Pod: {} to {} replicas".format(pod, replicas))
        
    def setPods(self, priorityPod, pods):
        self.priorityPod = priorityPod
        self.pods = pods
        
    def setValues(self, r):
        self.experiment = r["experiment"]
        self.name = r["name"]
        self.annotations = r["text"]
        self.priorityPod = r["priorityPod"]
        self.pods = r["pods"]
        self.slices = r["slices"]
    
    def start(self, r):
        self.setValues(r)
        text  = "Start experiment {}. {}".format(self.experiment, self.annotations)
        self.addAnnotation(text, True)
        self.fase = []
        
        if(self.debug):
            time.sleep(5)
            lFases = [1, 5]            
        else:
            lFases = [1, 5, 10, 15, 20, 25]
            time.sleep(30)
        
        self.scale(self.priorityPod, 4)
        self.startScale = datetime.now(timezone.utc)
        self.tStart = int( self.startScale.timestamp() * 1000)
        for fase in lFases:
            text = "{} - Fase {}".format(self.name, fase)
            self.fase.append(self.addAnnotation(text))
            for p  in self.pods:
                self.scale(p, fase)
                
            if(self.debug):
                time.sleep(30)
            else:
                time.sleep(self.time)
            
        self.stopPods()
        self.tFinish = int(self.addAnnotation("{} - Finished ".format(self.name), False, True) * 1000)
        self.fase.append(self.tFinish)
        print("StartAt: {}".format(self.startAt.strftime("%Y-%m-%dT%H:%M:%S.000Z")))
        print("EndAt: {}".format(self.endAt.strftime("%Y-%m-%dT%H:%M:%S.000Z")))
        
    def saveInfos(self, queries):
        
        base = {"experiment": self.experiment, "annotation": self.annotations, "startAt": self.startAt, "endAt": self.endAt, "fases": self.fase }
        start = self.startAt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end   = self.endAt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        for q in queries:
            metric = q['name']
            query  = q['q']
            apiEndpoint = "{}/api/v1/query_range?start={}&end={}&step=5s&query={}".format(self.prometheus, start, end, query)
            txt  = requests.get(apiEndpoint).text
            data = json.loads(txt)
            base[metric] = {"status": data["status"], "result": data["data"]["result"]}
        
        db = self.getDatabase("open5gs")
        db["experiments"].insert_one(base)
        
        self.gri.getImages(self.tStart, self.tFinish, self.name, self.name, self.slices)
        
    def stopPods(self):
        self.scale(self.priorityPod, 0)
        for p  in self.pods:
            self.scale(p, 0)
                
    def verifyRunning(self):
        v1 = client.CoreV1Api()
        pod_list = v1.list_namespaced_pod("open5gs")
        for pod in pod_list.items:
            if(pod.metadata.name.startswith("open5gs-ue0") and pod.status.phase == "Running"):
                return False
                    
        return True