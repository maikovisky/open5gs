import json
from bson.timestamp import Timestamp
from pymongo import MongoClient
import pandas as pd
from decimal import Decimal
from bson.datetime_ms import DatetimeMS



class ETL:
    
    def __init__(self, databaseUrl, db):
        self.databaseUrl = databaseUrl
        self.db = self.getDatabase(db)
        
    def getDatabase(self, database):        
        conn = MongoClient(self.databaseUrl)        
        return conn[database]
    
    
    def etlValues(self, values, firstFase, metadata, datatype="float"):
        ret = []
        t = []
        while len(values):
            v = values.pop(0)
            if(v[0] > firstFase):
                v.append(v[0])
                v[0] = v[0] - firstFase
                if datatype == "int":
                    v[1] = int(v[1])
                elif datatype == "decimal":
                    v[1] = Decimal(v[1]) if v[1] == "0" else float(0)
                else:
                    v[1] = float(v[1])
                
                t.append({"metadata": metadata, "timestamp": DatetimeMS(v[0] * 1000), "value": v[1]})
                ret.append(v)
            
        return ret, t
    
    def createMetadata(self, ametadata, metric, etype):
        metadata = {"type": etype, **ametadata, **metric}
        print(metadata)
        return metadata
    
    def etlData(self, net, firstFase, metadata, etype, datatype="float"):
        r = []
        t = []
        while len(net["result"]):
            m = net["result"].pop(0)
            metadata = self.createMetadata(metadata, m["metric"], etype)
            values, timeseries = self.etlValues(m["values"],  firstFase, metadata, datatype)
            r.append({"metric": m["metric"], "values": values})
            dbTS = self.db["ts"]
            dbTS.insert_many(timeseries)

        return r
    
    def getFirstFase(self, e):
        return e["fases"][0]
    
    def createBaseMetadata(self, c):
        metadata = { "experiment": c["experiment"], "number": c["number"] }
        return metadata
    
    def etl(self):
        collection = self.db["experiments"] 
        dbEtl = self.db["etl"]
        cursor = collection.find({"experiment": "01"})
        for c in cursor:     
           metadata = self.createBaseMetadata(c)    
           firstFase = self.getFirstFase(c)
           c['receive'] = self.etlData(c["receive"], firstFase, metadata, "receive")
           c['transmit'] = self.etlData(c["transmit"], firstFase, metadata, "transmit")
           c['latency'] = self.etlData(c["latency"], firstFase, metadata, "latency")
           c['cpu'] = self.etlData(c["cpu"], firstFase, metadata, "cpu")
           c['memory'] = self.etlData(c["memory"], firstFase, metadata, "memory", "int")

           dbEtl.update_one({'_id': c['_id']}, {"$set": c}, True)
           
           #print(receive)
           
        
        

#etl = ETL("mongodb://127.0.0.1:27020", "open5gs")
etl = ETL("mongodb+srv://maikovisky:MFIl9m0cgK9UorO9@open5gs.xm3nrzk.mongodb.net", "open5gs")
etl.etl()

