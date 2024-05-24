import json, requests, time
from pymongo import MongoClient
from datetime import datetime, timezone
from kubernetes import client, config
import os
from graphs import GraphanaGetRenderImage
import k8stools

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
        self.corePods = []   
        self.UPFPods = []
        self.URANSIMPods = []  
        self.pods = []
        self.time = 240

        self.gri = GraphanaGetRenderImage(grafanaUrl, dashUID)
        
    def setCorePods(self, corePods, UPFPods, URANSIMPods):
        self.corePods = corePods
        self.UPFPods = UPFPods
        self.URANSIMPods = URANSIMPods
        self.cpu = [0] * len(self.UPFPods)
        self.nice = [None] * len(self.UPFPods)
        
  
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

        print(self.grafanaUrl + "/api/annotations")
        r = requests.post(self.grafanaUrl + "/api/annotations", headers=header, data=json.dumps(body))
        if(r.status_code >= 300):
            print("{} Can't add anotation. {}".format(r.status_code, r.text))
        
        return int( t.timestamp() )   
    
    # def scale(self, pod, replicas):
    #     k8sApi = client.AppsV1Api()
    #     k8sApi.patch_namespaced_deployment_scale(name=pod, namespace=self.namespace, body={'spec': {'replicas': replicas}})
    #     #print("Pod: {} to {} replicas".format(pod, replicas))
        
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
        
        for i, v in enumerate(r["cpu"]):        
            self.cpu[i] = v
            
        if "nice" in r:
            for i, v in enumerate(r["nice"]):        
                self.nice[i] = v
    
    def start(self, r):
        self.setValues(r)
        text  = "Start experiment {}. {}".format(self.experiment, self.annotations)
        self.addAnnotation(text, True)
        self.fase = []
        
        if(self.debug):
            time.sleep(5)
            lFases = [1, 5]            
        else:
            lFases = [1, 5, 10, 15, 20]
            time.sleep(30)
        
        k8stools.scale(self.priorityPod, self.namespace, 4)

        self.startScale = datetime.now(timezone.utc)
        self.tStart = int( self.startScale.timestamp() * 1000)
        for fase in lFases:
            text = "{} - Fase {}".format(self.name, fase)
            self.fase.append(self.addAnnotation(text))
            for p  in self.pods:
                k8stools.scale(p, self.namespace, fase)
                
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
        
        aText = "Experiment {} - {}".format(self.experiment, self.gri.getLatest())
        self.gri.getImages(self.tStart, self.tFinish, self.name, aText, self.slices)
        
        base = {"experiment": self.experiment, "number": self.gri.getLatest(),"annotation": self.annotations, "startAt": self.startAt, "endAt": self.endAt, "fases": self.fase }
        start = self.startAt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end   = self.endAt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        for q in queries:
            metric = q['name']
            query  = q['q']
            apiEndpoint = "{}/api/v1/query_range?start={}&end={}&step=5s&query={}".format(self.prometheus, start, end, query)
            txt  = requests.get(apiEndpoint).text
            data = json.loads(txt)
            base[metric] = {"status": data["status"], "result": data["data"]["result"]}

                
        db = self.getDatabase("open5gsNice")
        db["experiments"].insert_one(base)
        
    
    def stopOpen5gsCore(self):
        for p in self.URANSIMPods[::-1]:
            k8stools.scale(p, self.namespace, 0)
            
        for p in self.UPFPods[::-1]:
            k8stools.scale(p, self.namespace, 0)
            
        for p in self.corePods[::-1]:
            k8stools.scale(p, self.namespace, 0)
            
    def startOpen5gsCore(self):
        for p in self.corePods:
            k8stools.scale(p, self.namespace, 1)
            time.sleep(2)
            
        for p in self.UPFPods:
            k8stools.scale(p, self.namespace, 1)
            time.sleep(2)
            
        for p in self.URANSIMPods:
            k8stools.scale(p, self.namespace, 1)
            time.sleep(2)
    
    def resetCore(self, wait=False):
        print("Resetando core")
        self.stopOpen5gsCore()
        time.sleep(10)
        

        print(self.cpu)
        for i, p in enumerate(self.UPFPods):
            k8stools.setEnv(self.namespace, p, "NICE_VALUE", self.nice[i])
            k8stools.update_resource(self.namespace, p, self.cpu[i], self.cpu[i])

            
        
        self.startOpen5gsCore()
        print("Esperando core subir")
        self.verifyCoreRunnig()
        
    def stopPods(self):
        k8stools.scale(self.priorityPod, self.namespace, 0)
        for p  in self.pods:
            k8stools.scale(p, self.namespace, 0)
                
    def verifyCoreRunnig(self):
        v1 = client.CoreV1Api()
        notRunning = True
        while(notRunning):
            ret = v1.list_namespaced_pod("open5gs", watch=False)
            podsFound = []
            notRunning = False
            for i in ret.items:
                name = "-".join(i.metadata.name.split("-")[0:-2])

                if(i.status.phase == "Running" and name in self.corePods):
                    podsFound.append(name)
                
                if(i.status.phase == "Running" and name in self.UPFPods):
                    podsFound.append(name)
                    
                if(i.status.phase == "Running" and name in self.URANSIMPods):
                    podsFound.append(name)
                    
            if(not set(self.corePods).issubset(podsFound)):
                print("Esperando core Open5GS estarem operando")
                notRunning = False
                            
            if(not set(self.UPFPods).issubset(podsFound)):
                print("Esperando UPFs Open5GS estarem operando")
                notRunning = False
                
            if(not set(self.URANSIMPods).issubset(podsFound)):
                print("Esperando URANSIM Open5GS estarem operando")
                notRunning = False
                
            if(not notRunning):
                time.sleep(15)


                
    def verifyRunning(self):
        v1 = client.CoreV1Api()
        pod_list = v1.list_namespaced_pod("open5gs")
        for pod in pod_list.items:
            if(pod.metadata.name.startswith("open5gs-ue0") and pod.status.phase == "Running"):
                return False
                    
        return True