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
df_base = pd.read_csv("/home/monica.marmit/sample.csv")

def get_gcp_academy_data(userid,creds = '/home/anuragverma/challenges/.gcp_key_competencyassessment.json'):
        from google.cloud import bigquery
        import os, json
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
        bq_client = bigquery.Client()
        query="""
with view1 as (select distinct eventid from `competencyassessment.assessment.event_users` where userid = '{}' limit 1)
select eventid, userid, case 
when questionid in ("42bbd29c-6e24-49f1-8a0e-734bdf7773d3","d39ec9e4-3862-4f56-8616-74af8b4c1124", "b4592c38-9217-469e-95a0-d1f9361b0e1d","7a5fd7e4-a4a6-45c8-b7db-4945b3338ba4", "73f873a5-5b39-4442-8538-d4ff9bbcac2d","4feddbdb-7f96-448a-9bf9-3a3647d9846e", "1194d17e-e7bf-4857-ab38-446bbb1d5458","73251400-2176-4084-ab07-fb10b13b9695", "e447a25e-aabc-4f6f-b9e0-6e1da20eef99","02ef00b5-bec6-434a-9e7f-8a3131c043d6") then 'Cloud SQL' 
when questionid in ("f1f6e2c8-3b7e-4c42-b19d-89e26071f687","e6c7aa19-8600-41fd-82c9-f1e51b093ea9", "dd254173-ebd2-407a-93fc-ab62d16aec24","ebd3ab8b-b360-43bb-be98-90b1b5ad6a9c", "dfd70c22-bc0e-4408-9bf6-6a2a386096bc","136343ac-b2b1-4f14-8a31-e171476ac4eb", "ce6ce861-7af3-4649-ac52-c5e87455808b","7404e7a7-9920-47f7-b74f-dc89e3bc6412") then 'Big Query' 
when questionid in ("f50ec0b7-f960-400d-91f0-c42a6d44e3d0","bd65600d-8669-4903-8a14-af88203add38") then 'Storage' 
when questionid in ("26cb4df2-3e90-4495-b4b2-5ec0b2a07854","c573d88e-467e-43fa-809e-bbcf06f46454", "85745ab8-e812-42b8-8444-bd1acdf0677a","65471199-686d-4035-b049-c75b23f88f6f", "b9491a28-c863-4f8d-9cac-a0d4395e99dc","2521993c-6731-4136-8926-6127ebcc8a06") then 'Dataproc'
when questionid in ("f50ec0b7-f960-400d-91f0-c42a6d44e3d0","bd65600d-8669-4903-8a14-af88203add38") then 'Dataflow' 
when questionid in ("10c62efd-7a11-4efa-9db2-cc29f8be1673","a4179765-ef2f-4bb2-a17b-f7548f64529a", "66ba575d-9658-48b8-81ae-59af98b3decf","23b41559-1acc-4e6d-990f-6d0c5869665c") then 'Data Fusion'
when questionid in ("43ea5e5b-2d7f-4311-8834-22a205fe0981","87fdbfb2-4527-4882-9493-f00fe81bbd87") then 'Composer'
else 'Others'
end as service,
questionid, max(score) as score, count(1) as attempts
from `competencyassessment.assessment.scores`
where eventid in (select * from view1)
group by eventid, userid, questionid""".format(userid)
        query_job = bq_client.query(query)
        result = [dict(row) for row in query_job]
        return json.dumps(result)


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
    return df

columns11 = [
{"name":["","Participant Name"],"id":"participant_id"},
{"name":["","Score"],"id":"Total_Score"},
{"name":["","Submission"],"id":"Total_Submissions"},
{"name":["Medals","Gold"],"id":"Gold_Medals"},
{"name":["Medals","Silver"],"id":"Silver_Medals"},
{"name":["Medals","Bronze"],"id":"Bronze_Medals"},
{"name":["Medals","Top 5"],"id":"Top_5"},
{"name":["Medals","Top 10"],"id":"Top_10"}
]

df11 = overall(df_base)
#df_event = event(df_base,eventid)
#df_individual = individual(df_base,p_id)

df21 = event(df_base,'20210906')
columns21 = [
        ]

df31 = None
columns31 = [
{"name":["Event"],"id":"eventid"},
{"name":["Participant Name"],"id":"userid"},
{"name":["GCP Service"],"id":"service"},
{"name":["Question"],"id":"questionid"},
{"name":["Score"],"id":"score"},
{"name":["Attempts"],"id":"attempts"},
]

df41 = df_base
columns41 = [
        ]

df51 = df_base
columns51 = [
        ]

df61 = df_base
columns61 = [
        ]


col11 = [i['id'] for i in columns11]
col21 = [i['id'] for i in columns21]
col31 = [i['id'] for i in columns31]
col41 = [i['id'] for i in columns41]
col51 = [i['id'] for i in columns51]
col61 = [i['id'] for i in columns61]

