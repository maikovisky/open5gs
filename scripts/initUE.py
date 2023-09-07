from pymongo import MongoClient
import json
import os
import psutil
import socket
import struct
import random

from pydantic import TypeAdapter, ValidationError

print(TypeAdapter(bool).validate_python('yes'))  
print(TypeAdapter(bool).validate_python('no'))  

exit
IMSI = os.environ.get("IMSI", "999700000000000")
CREATE_IMSI = os.environ.get("CREATE_IMSI", True)
CREATE_NEW_IMSI = os.environ.get("CREATE_NEW_IMSI", False)
USE_IMSI_NETWORK = os.environ.get("USE_IMSI_NETWORK", False)

def getDatabase(database):
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb://localhost:27017/open5gs")
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    conn = MongoClient(DATABASE_URL)
    return conn[database]


def verifyIMSI(IMSI):
    db = getDatabase("open5gs")
    if( db["subscribers"].count_documents({"imsi": IMSI}) != 0 ):
        return True
    
    return False

def addIMSI():
    db = getDatabase("open5gs")
    last = db["subscribers"].find({}).sort("_id", -1).limit(1)
    lastIMSI = int(last[0]["imsi"]) + 1
    addSubscribers(lastIMSI)
    return lastIMSI

def addSlice(name, sst, sd):
    slice = {"sst" : sst, "sd" : sd, "default_indicator" : True, "session" : [
                {"name" : name, "type" : 3,"pcc_rule" : [],  "ambr" : { "uplink" : {"value" : 1,"unit" : 3}, "downlink" : { "value" : 1,"unit" : 3}},
                    "qos" : {"index" : 9, "arp" : { "priority_level" : 8,"pre_emption_capability" : 1, "pre_emption_vulnerability" : 1} }}
            ]}
    print(slice)
    return slice


def randomSlice():
    sst = random.randint(1,4)
    sd  = str(sst).rjust(6, "0")
    name = "slice" + str(sst).rjust(2, "0")
    return name, sst, sd

def addSubscribers(IMSI):
    
    db = getDatabase("open5gs")
    base = {"imsi" : IMSI,  "subscribed_rau_tau_timer" : 12, "network_access_mode" : 0, "subscriber_status" : 0, "access_restriction_data" : 32}
    ambr = { "uplink" : {"value" : 1, "unit" : 3 },"downlink" : { "value" : 1,"unit" : 3} }
    security = {"k" : "465B5CE8B199B49FAA5F0A2EE238A6BC","amf" : "8000","op" : None, "opc" : "E8ED289DEBA952E4283B54E88E6183CA","sqn" : 1153 }
    values   = {"purge_flag" : [], "mme_realm" : [], "mme_host" : [], "imeisv" : "4370816125816151", "msisdn" : [], "schema_version" : 1,"__v" : 0}

    name, sst, sd = randomSlice()
    s = addSlice(name, sst, sd)

    slice = [{"sst" : 1, "default_indicator" : True, "session" : [
                {"name" : "internet", "type" : 3,"pcc_rule" : [],  "ambr" : { "uplink" : {"value" : 1,"unit" : 3}, "downlink" : { "value" : 1,"unit" : 3}},
                    "qos" : {"index" : 9, "arp" : { "priority_level" : 8,"pre_emption_capability" : 1, "pre_emption_vulnerability" : 1} }}
            ]}]
    slice.append(s)
    
    
    ns = {**base, "slice": slice, "ambr": ambr, "security": security, **values }
    
    db["subscribers"].insert_one(ns)
    
def get_ipv4_from_nic(interface):
    interface_addrs = psutil.net_if_addrs().get(interface) or []
    for snicaddr in interface_addrs:
        if snicaddr.family == socket.AF_INET:
            return snicaddr.address

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]
        
if(USE_IMSI_NETWORK):
    addr = get_ipv4_from_nic("eth0")
    IMSI = str(int(IMSI) + ip2int(addr))

if(not verifyIMSI(IMSI) and CREATE_IMSI):
    addSubscribers(IMSI)
elif (CREATE_NEW_IMSI):
    IMSI = addIMSI(IMSI)
    
print(IMSI)