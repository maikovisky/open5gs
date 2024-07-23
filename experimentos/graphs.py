
import json, requests, os
import shutil
from requests.exceptions import ConnectionError

# - latency: 62
# - cpu: 50
# - Memory: 7
# - Data plane: 54
# - Data control: 70
# - UE: 71
# - Pods: 60
# - Sessions: 46

panels = json.loads("""[
    {"panelId": "7",  "name": "memory"},                       
    {"panelId": "50", "name": "cpu"},                       
    {"panelId": "62", "name": "latency"},                       
    {"panelId": "72", "name": "dataPlane"},                       
    {"panelId": "70", "name": "dataControl"},
    {"panelId": "71", "name": "ue"},
    {"panelId": "60", "name": "pods"},
    {"panelId": "46", "name": "upfSessions"},
    {"panelId": "69", "name": "receive"},
    {"panelId": "55", "name": "transmit"},
    {"panelId": "73", "name": "receive_packets_drop"},
    {"panelId": "74", "name": "transmit_packets_drop"},
    {"panelId": "75", "name": "receive_iperf"}
]""")


class GraphanaGetRenderImage:
    
    def __init__(self, graphanaUrl, dashboardUI, path="experimentos", subpath="exp"):
        self.graphanaUrl = graphanaUrl
        self.path = path
        self.dashboardUI = dashboardUI
        self.subpath = subpath
        self.latest  = "0001"

    def getUrl(self, slices):
        #base = "orgId=1&var-datasource=prometheus&var-cluster=&var-namespace=open5gs&var-resolution=30s&var-intervalo=1m&var-data_plane=open5gs-upf-1&var-ues=open5gs-ue01&var-workload=open5gs-iperf01&var-interface=eth0&var-interface=slice01&var-irate=1m&from=1711543859370&to=1711545539107&var-data_control=open5gs-amf&var-data_control=open5gs-ausf&var-data_control=open5gs-bsf&var-data_control=open5gs-nrf&var-data_control=open5gs-nssf&var-data_control=open5gs-pcf&var-data_control=open5gs-scp&var-data_control=open5gs-smf&var-data_control=open5gs-udm&var-data_control=open5gs-udr&theme=light&panelId=62&width=2000&height=600&tz=America%2FSao_Paulo"
        base = "orgId=1&var-datasource=prometheus&var-cluster=&var-namespace=open5gs&var-resolution=30s&var-intervalo=2m&var-irate=2m&var-interval=2m&theme=light&width=2000&height=600&tz=America%2FSao_Paulo"
        urlConfig = self.getUrlConfig(slices)
        url = "{}/render/d-solo/{}/open-5g?{}&{}".format(self.graphanaUrl, self.dashboardUI, base, urlConfig)
        return url
    
    def getUrlConfig(self, slices):
        #interface = "var-interface=eth0"
        dp = []
        for s in slices:
            sPad =  s.rjust(2, "0")
            dp.append("var-data_plane=open5gs-upf-{}".format(s))
            dp.append("var-ues=open5gs-ue{}".format(sPad))
            dp.append("var-workload=open5gs-iperf{}".format(sPad))
            dp.append("var-interface=slice{}".format(sPad))
            
        vars = '&'.join(dp)
        
        #url = "var-datasource=prometheus&var-cluster=&var-namespace=open5gs&var-data_plane=open5gs-upf-1&var-ues=open5gs-ue01&var-workload=open5gs-iperf01&var-interface=eth0&var-interface=slice01&from=1711543859370&to=1711545539107&var-data_control=open5gs-amf&var-data_control=open5gs-ausf&var-data_control=open5gs-bsf&var-data_control=open5gs-nrf&var-data_control=open5gs-nssf&var-data_control=open5gs-pcf&var-data_control=open5gs-scp&var-data_control=open5gs-smf&var-data_control=open5gs-udm&var-data_control=open5gs-udr"
        url = "var-data_control=All&{}".format(vars)
        return url
    
    def createPath(self, path, name, subpath="exp"):
        basePath = "{}\\{}".format(path, name)
        if not os.path.exists(basePath):            
            basePath = "{}\\{}0001".format(basePath, subpath)
            self.latest = "0001"
            os.makedirs(basePath)
        else:    
            all_folders = os.listdir(basePath)
            all_folders.sort(reverse=True)
            first = all_folders[0]
            self.latest = str(int(first.replace(subpath, '')) + 1).rjust(4, "0")
            
            basePath = "{}\\{}{}".format(basePath, subpath, self.latest)
            #print(basePath)
            os.makedirs(basePath)

        return basePath
    
    def getLatest(self):
        return self.latest

    def getImages(self, start, end,  name, aText, slices = ["1"]):        
        global panels
        headers = {'Content-Type': 'application/json','accept': 'application/json'}

        url = self.getUrl(slices)
        basePath = self.createPath(self.path, name, self.subpath)
        text = "({})".format(aText)
        txtFilename = "{}\\{}-grafana.txt".format(basePath, name)
        for p in panels:
            finalUrl = "{}&from={}&to={}&panelId={}&var-experience={}".format(url, start, end, p["panelId"], text)
            #print(finalUrl)
            filename = "{}\\{}-{}.png".format(basePath, name, p["name"])
            #print("Create: {}".format(filename))
            try:
                response = requests.get(finalUrl, stream=True, headers=headers)
            except ConnectionError as e:
                print("Can't request.get({})".format(finalUrl))
                print(e.strerror)
                
            with open(filename, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            with open(txtFilename, 'a+') as f:
                f.write(finalUrl)
                f.write("\n")
    
    def downloadImages(self, start, end, name, text, slices, sequence):
        global panels
        url = self.getUrl(slices)
        basePath = basePath = "{}\\{}\\{}{}".format(self.path, name,  self.subpath, sequence)
        if not os.path.exists(basePath): 
            os.makedirs(basePath)
            
        for p in panels:
            finalUrl = "{}&from={}&to={}&panelId={}&var-experience={}".format(url, start, end, p["panelId"], text)
            #print(finalUrl)
            filename = "{}\\{}-{}.png".format(basePath, name, p["name"])
            #print("Create: {}".format(filename))
            response = requests.get(finalUrl, stream=True)
            with open(filename, 'wb') as file:
                shutil.copyfileobj(response.raw, file)

