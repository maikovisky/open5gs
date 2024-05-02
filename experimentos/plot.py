#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
import plotly.io as pio 
import plotly.graph_objects as go

pio.kaleido.scope.mathjax = None


conn = MongoClient("mongodb+srv://maikovisky:MFIl9m0cgK9UorO9@open5gs.xm3nrzk.mongodb.net")  
    
db = conn["open5gs"]
col = db["ts"]

#cursor = col.find()

pipeline = [
    { "$match": { "metadata.type": "receive", "metadata.experiment": "01", "metadata.interface": "eth0", "metadata.workload":  {"$in": ["open5gs-upf-1", "open5gs-upf-2"]} }},
    { "$group": {
        "_id": {
           "interface": "$metadata.interface",
           "workload": "$metadata.workload",
           "timestamp": { "$dateTrunc": {"date": "$timestamp", "unit": "second", "binSize": 30}}
        },
        "value": { "$avg": "$value"},
        "count": { "$count": {}}
    }},
    { "$sort": { "_id.timestamp": 1}},
    { "$project": {
        "_id": 0,
        "timestamp": "$_id.timestamp",
        "interface": "$_id.interface",
        "workload": "$_id.workload",
        "value": 1,
        "count": 1
    }}
]

cursor = col.aggregate(pipeline)
df = pd.DataFrame(list(cursor))
print(df)    
    
#fig = go.Figure()
fig = px.line(df, x="timestamp", y="value", color='workload', title="Receive UPF")


fig.update_xaxes(tickformat='%H:%M', title="", zeroline=True, zerolinecolor="#FF0000")
fig.update_yaxes(linewidth=1, title="Bandwith", zeroline=True, zerolinecolor="#FF0000", zerolinewidth=2)
fig.update_layout(
   legend_orientation='h',
   width=2000, 
   height=750,
   legend_title_text="",
   margin_r=10,
   plot_bgcolor="#eeeeee",
   title_font_family="verdana",
)

fig.write_image("fig3.png")