# base_data.py
import dash_html_components as html
from flask import current_app
import os
import base64
from datetime import datetime
from pathlib import Path
DATA_DIR = current_app.config['DATA_DIR']

import numpy as np
import pandas as pd
df21 = pd.read_csv("/home/monica.marmit/sample.csv")


def individual(df,p_id):
    #df = pd.read_csv(sample_file)
    df = df[df['participant_id']==p_id]
    df = df.sort_values(by=['Rank']).reset_index(drop=True).drop("participant_id",axis=1)
    return df


from collections import Counter
def func(x):return dict(Counter(list(x)))
 

def overall(df):
    df["gm"] = np.where(df["Rank"]==1, 1, 0)
    df["sm"] = np.where(df["Rank"]==2, 1, 0)
    df["bm"] = np.where(df["Rank"]==3, 1, 0)
    df["T5"] = np.where(((df["Rank"]>3)&(df["Rank"]<6)), 1, 0)
    df["T10"] = np.where(((df["Rank"]>5)&(df["Rank"]<11)), 1, 0)
    df1 = df.groupby("participant_id").agg(Total_Score=("Score","sum"), Total_Submissions=("no_subm","sum"), 
        Gold_Medals = ("gm","sum"), Silver_Medals = ("sm","sum"), Bronze_Medals = ("bm","sum"), Top_5 = ("T5","sum"), Top_10 = ("T10","sum")).reset_index()
    return df1


def event(df,eventid):
    #df = pd.read_csv(sample_file)
    df = df[df['Eventid']==eventid]
    df = df.sort_values(by=['Rank']).reset_index(drop=True).drop("Eventid",axis=1)
    return d

columns_overall = [
{"name":["","Participant Name"],"id":"participant_id"},
{"name":["","Score"],"id":"Total_Score"},
{"name":["","Submission"],"id":"Total_Submissions"},
{"name":["Medals","Gold"],"id":"Gold_Medals"},
{"name":["Medals","Silver"],"id":"Silver_Medals"},
{"name":["Medals","Bronze"],"id":"Bronze_Medals"},
{"name":["Medals","Top 5"],"id":"Top_5"},
{"name":["Medals","Top 10"],"id":"Top_10"}
]

df_overall = overall(df21)
#df_event = event(df21,eventid)
#df_individual = individual(df21,p_id)


