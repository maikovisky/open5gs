
conn = new Mongo("mongodb://localhost:27020/"); 
db = conn.getDB("open5gs");
doc = db.subscribers.findOne({ "$or": [{"isUsed": false},  {"isUsed": { "$exists": true }} ]});

printjson( doc );
if(doc == null) {
    console.log("No IMSI");
}

