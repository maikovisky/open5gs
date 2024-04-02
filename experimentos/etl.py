import json
from pymongo import MongoClient
import pandas as pd




class ETL:
    
    def __init__(self, databaseUrl, db):
        self.databaseUrl = databaseUrl
        self.db = self.getDatabase(db)
        
    def getDatabase(self, database):        
        conn = MongoClient(self.databaseUrl)        
        return conn[database]
    
    def getLatencyTimestamp(self):
        collection = self.db["experiments"]
        cursor = collection.find()
        df = pd.json_normalize(cursor["latency"])
        print(df)
        return
        




etl = ETL("mongodb://127.0.0.1:27020", "open5gs")
etl.getLatencyTimestamp()

