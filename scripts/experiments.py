from pymongo import MongoClient
import paho.mqtt.client as mqtt
import time
import json
import pandas as pd   
from threading import Lock 


unit = {0: "bps", 1: "Kbps", 2: "Mbps", 3: "Gbps", 4: "Tbps"}
enable={1: "disable", 2: "enable"}
mqttWaiting=True
client = mqtt.Client()
lock = Lock()
ue = 0
ex = {}
df = pd.DataFrame()
dfSlice = pd.DataFrame()
dfIMSI    = pd.DataFrame()
dfFinish  = pd.DataFrame()
numUE = 0
status="config"

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27020/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['open5gs']

def on_connect(client, userdata, flags, rc):
    global status
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    status = "clean"
    client.subscribe("#", 0) 
    client.loop_start()
    

def on_disconnect(client, userdata, rc):
    print("Disconnect with result code "+str(rc))
    
def verifyUE(topic, msg):
    global slices
    global dfSlice
    global dfIMSI
    global numUE
    flag = False
    print("Topic: " + topic)
    with lock:
        data = json.loads(msg.payload)
        df1 = pd.json_normalize(data)
        
        if hasUE(slice, dfSlice, dfIMSI, numUE):
            dfIMSI = dfIMSI._append(df1)
            flag = True
            client.publish(topic, "{\"status\": \"ok\"}")
            print("Permit " + df1["imsi"])
        else:
            client.publish(topic, "{\"status\": \"nok\"}") 
            print("Recuse " + df1["imsi"])
        
    return flag

def verifyFinish(topic, msg):
    global numUE
    global dfFinish
    print("verifyFinish Topic: " + topic + " MSG: " + str(msg.payload))
    data = json.loads(msg.payload)
    df1 = pd.json_normalize(data)
    dfFinish = dfFinish._append(df1)
    
    if(len(dfFinish) >= numUE):
        return True
    return False

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global slices
    global dfIMSI
    global numUE
    global mqttWaiting
    global status
    
    if status == "clean":
        print("Clean..")
        client.unsubscribe("#")
        status = "config"
        return
    
    print("Nova mensagem: " + msg.topic+" "+str(msg.payload))
    topic = msg.topic #.split("/", 1)
    time.sleep(2)
    #res = list(filter(lambda slices: slices['name'] == topic[0], slices)) 
    
    if status == "config":
        verifyUE(topic, msg)
            
        if len(dfIMSI) >= numUE:
            print("UEs done")
            mqttWaiting=False
            #client.loop_stop(force=False)
    
    if status == "run":
        if verifyFinish(topic, msg):
            print("UEs Finished")
            mqttWaiting=False


def startExperiment(e, numUe):
    global slices
    global mqttWaiting
    global lock
    global status
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect("127.0.0.1", 1884, 60)
    time.sleep(3)
    
    
    cmdAll = "-t " + str(e['time']) + " "
    for c in e['cmds']:
        cmd = cmdAll + c     
        slices = e['slices']  
        mqttWaiting = True    
        with lock:    
            for s in slices:
                #print(s['name']+"/ue/#")
                client.subscribe(s['name']+"/ue/#", 0) 
                client.publish(s['name'], "{\"status\": \"config\", \"cmd\": \""+ cmd + "\"}") 
                               
        # client.subscribe("slice01/ue", 2)
        
        while mqttWaiting:
            print("Waiting UE " + time.ctime() + " " + str(mqttWaiting))
            for s in slices:
                client.publish(s['name'], "{\"status\": \"config\", \"cmd\": \""+ cmd + "\"}") 
            time.sleep(5)
            
        #client.loop_forever()
        status = "run"
        
        time.sleep(5)
        client.publish("start", "start", 0)
        client.subscribe("finish", 0)
        #client.loop_start()
        mqttWaiting = True
        while mqttWaiting:
            print("Waiting finish: " + time.ctime() + " " + str(mqttWaiting))
            client.publish("start", "start", 0) 
            time.sleep(5)
            
        status = "config"

def updateSliceAmbr(s, ambr):
    db = get_database()
    subscribers = db["subscribers"]
    subscribers.update_many(
        {"slice.session.name": s},
        {"$set": {"slice.$.session.0.ambr": ambr }}
    )
    
def updateSliceQoS(s, qos):
    db = get_database()
    subscribers = db["subscribers"]
    subscribers.update_many(
        {"slice.session.name": s},
        {"$set": {"slice.$.session.0.qos": qos }}
    )
       
def hasUE(slice, dfSlice, dfIMSI, maxUE):
    if not len(dfSlice) and len(dfIMSI) < maxUE:
        return True
    
    if len(dfSlice) <= 0:
        return False
    
    dfS = dfSlice.set_index('slice')

    if slice not in dfS.index:
        return False

    if len(dfIMSI) == 0:
        return True

    dfAtive = dfIMSI.groupby(['slice']).count()
    dfJoin = dfS.join(dfAtive)
    dfRet= dfJoin.query('imsi < ue')
    if slice in dfRet.index:
        return True
    return False
       
def sliceAmbr(s, ambr):
    if("ambr" in s):
        print("\tUplink..: " + str(s['ambr']['uplink']['value']) + " " + unit.get(s['ambr']['uplink']['unit']))
        print("\tDownlink: " + str(s['ambr']['downlink']['value']) + " " + unit.get(s['ambr']['downlink']['unit']))
        updateSliceAmbr(s['name'], s['ambr'])
    else:
        print("\tUplink..: " + str(ambr['uplink']['value']) + " " + unit.get(ambr['uplink']['unit']))
        print("\tDownlink: " + str(ambr['downlink']['value']) + " " + unit.get(ambr['downlink']['unit']))
        updateSliceAmbr(s['name'], ambr)
        
def sliceQoS(s, qos):
    if("qos" in s):
        print("\t5QI/QCI...........: " + str(s['qos']['index']))
        print("\tARP Priority Level: " + str(s['qos']['arp']['priority_level']))
        print("\tCapability........: " + enable.get(s['qos']['arp']['pre_emption_capability']))
        print("\tVulnerability.....: " + enable.get(s['qos']['arp']['pre_emption_vulnerability']))
        updateSliceQoS(s['name'], s['qos'])
    else:
        print("\t5QI/QCI*: " + str(qos['index']))
        print("\tARP Priority Level: " + str(qos['arp']['priority_level']))
        print("\tCapability........: " + enable.get(qos['arp']['pre_emption_capability']))
        print("\tVulnerability.....: " + enable.get(qos['arp']['pre_emption_vulnerability']))
        updateSliceQoS(s['name'], qos)

def slice(s, ambr, qos):
    print("Slice: " + s['name'])
    sliceAmbr(s, ambr)
    sliceQoS(s, qos)


def experiments(e):
    global dfSlice
    global numUE
    
    print("==========================================================================")
    print("Inicio: " + e['name'] + " rodando por " + str(e['time']) + " s")
    print("\t" + e['description'])
    numUE = 0
    for s in e['slices']:
        slice(s, e['ambr'], e['qos'])  
        if "ue" in s: 
            numUE = numUE + s['ue']
            dfSlice = dfSlice._append({"slice": s['name'], "ue":  s['ue']}, ignore_index=True)
            print(dfSlice)
        else:
            numUE = numUE + e['ue']

    print("\tUE Total: " + str(numUE))
    startExperiment(e, numUE)
    
    

db = get_database()
collection = db["experiments"].find()

for r in collection:
    dfIMSI    = pd.DataFrame()
    dfFinish  = pd.DataFrame()
    dfSlice   = pd.DataFrame()
    experiments(r)

print("==========================================================================")

