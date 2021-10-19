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

def get_active_event_data(userid,creds = '/home/anuragverma/challenges/.gcp_key_competencyassessment.json'):
        from google.cloud import bigquery
        import os, json
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
        bq_client = bigquery.Client()
        query="""WITH active_events as (select distinct e.eventid, e.event_start  from 
competencyassessment.assessment.event_users eu 
join competencyassessment.assessment.event e 
on eu.eventid = e.eventid where active and userid='{}')
,event_teams as (select a.eventid,team,string_agg(userid, ", ") as members
from active_events a 
join competencyassessment.assessment.event_users eu 
on a.eventid = eu.eventid
group by eventid,team),
interim as (select sc.eventid,et.members,sc.team,sc.questionid,description, count(1) as attempts,
(   case when value3 = 'maximum' then max(score)
    when value3='minimum' then min(score)
    else NULL end) as score,
(case when value3 ='maximum' then -1 else 1 end ) as sort 
from competencyassessment.assessment.scores sc
join competencyassessment.assessment.questions q on sc.questionid = q.questionid
join active_events a on sc.eventid = a.eventid
join event_teams et on et.eventid=a.eventid and sc.team = et.team
where cast(time as timestamp) > event_start
group by sc.eventid,et.members,sc.team,sc.questionid,description, value3)
select * , rank() over(partition by eventid, questionid order by score*sort, attempts desc) as rank from interim
order by score*sort, attempts desc
""".format(userid)
        query=query.replace("\n"," ")
        query=query.replace("  "," ")
        query_job = bq_client.query(query)
        result = [dict(row) for row in query_job]
        return json.dumps(result)

def get_completed_event_data(userid):
    return None


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
{"name":["Rank"],"id":"rank"},
{"name":["Team"],"id":"team"},
{"name":["Members"],"id":"members"},
{"name":["Best Score"],"id":"score"},
{"name":["Attempts"],"id":"attempts"},
]


columns31 = [
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


