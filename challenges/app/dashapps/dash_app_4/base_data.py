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

EVENTLIST=['MDSC00','MDSC01','MDSC02']

MANUAL_QUESTIONID={'MDSC00':'783b0bed-7c51-40ac-90f8-38434d51c40b','MDSC01':'ce706c03-dcf5-405d-9cc5-d132d4cd5824','MDSC02':''}

QUESTIONID_DESC={'783b0bed-7c51-40ac-90f8-38434d51c40b':'Exec Summary for MDSC00','ce706c03-dcf5-405d-9cc5-d132d4cd5824':'Exec Summary for MDSC01','':'Exec Summary for MDSC02'}

def get_manual_evaluation_data(eventid,questionid,creds = '/home/anuragverma/challenges/.gcp_key_competencyassessment.json'):
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
        return json.dumps(result,default=str)

def get_completed_event_data(creds = '/home/anuragverma/challenges/.gcp_key_competencyassessment.json'):
        from google.cloud import bigquery
        import os, json
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
        bq_client = bigquery.Client()
        query="""WITH event_teams as 
(select e.eventid,eu.team,string_agg(userid, ", ") as members, max(event_name) as description
from `competencyassessment.assessment.event_users` eu
join `competencyassessment.assessment.event` e
on eu.eventid = e.eventid
where e.eventid like "MDSC%"
group by e.eventid, team),
last_scores as
(select eventid, team, category , score, row_number() over(partition by eventid, team, category order by updated desc) as rank
from `competencyassessment.assessment.final_scores`
),
interim as 
(select et.eventid, et.team, et.members, et.description,
sum(case when category = "Absolute" then score else 0 end) as model_abs,
sum(case when category = "Relative" then score else 0 end) as model_rel,
sum(case when category = "Content" then score else 0 end) as exec_sum_con,
sum(case when category = "Format" then score else 0 end) as exec_sum_form,
sum(score) as total_score
from last_scores ls 
join event_teams et 
on ls.eventid = et.eventid
and ls.team=et.team
where rank =1
group by et.eventid, et.team, et.members, et.description)
select *, rank() over (partition by eventid order by total_score desc) as rank
from interim 
        """
        query=query.replace("\n"," ")
        query=query.replace("  "," ")
        query_job = bq_client.query(query)
        result = [dict(row) for row in query_job]
        return json.dumps(result,default=str)


def get_my_submission_data(userid,creds = '/home/anuragverma/challenges/.gcp_key_competencyassessment.json'):
        from google.cloud import bigquery
        import os, json
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
        bq_client = bigquery.Client()
        query="""
        select sc.eventid, sc.userid, sc.questionid, sc.team, sc.score, sc.time, q.description
from competencyassessment.assessment.scores sc
join competencyassessment.assessment.questions q
on sc.questionid = q.questionid
where userid='{}' and eventid like 'MDSC%'
        """.format(userid)
        query=query.replace("\n"," ")
        query=query.replace("  "," ")
        query_job = bq_client.query(query)
        result = [dict(row) for row in query_job]
        return json.dumps(result,default=str)

def overall(df_in):
	#df_in=pd.read_json(js)[['members','rank','total_score']]
	df_in['participant_list']=df_in.apply(lambda x : x['members'].split(','),axis=1)
	df=df_in.explode('participant_list')
	df['participant_id']=df['participant_list'].str.strip()
	df["gm"] = df.apply(lambda x : 1 if x["rank"]==1 else 0, axis=1)
	df["sm"] = df.apply(lambda x : 1 if x["rank"]==2 else 0, axis=1)
	df["bm"] = df.apply(lambda x : 1 if x["rank"]==3 else 0, axis=1)
	df["T5"] = df.apply(lambda x : 1 if (x["rank"] >= 4 and x["rank"] <=5) else 0, axis=1)
	df["T10"] = df.apply(lambda x : 1 if (x["rank"] >= 6 and x["rank"] <=10) else 0, axis=1)
	df1 = df.groupby("participant_id").agg(total_score=("total_score","sum"), 
	        gm = ("gm","sum"), sm = ("sm","sum"), bm = ("bm","sum"), T5 = ("T5","sum"), T10 = ("T10","sum")).reset_index().sort_values('total_score',ascending=False)
	return df1


columns11 = [
{"name":["Rank"],"id":"rank"},
{"name":["Team"],"id":"team"},
{"name":["Members"],"id":"members"},
{"name":["Best Model Metric"],"id":"score"},
{"name":["Attempts"],"id":"attempts"},
]

columns21 =[
{"name":["","Rank"],"id":"rank"},
{"name":["","Team"],"id":"team"},
{"name":["","Members"],"id":"members"},
{"name":["Modeling","Absolute"],"id":"model_abs"},
{"name":["Modeling","Relative"],"id":"model_rel"},
{"name":["Summary","Content"],"id":"exec_sum_con"},
{"name":["Summary","Format"],"id":"exec_sum_form"},
{"name":["Total","Points"],"id":"total_score"},
        ]


columns31 = [
{"name":["","Participant Name"],"id":"participant_id"},
{"name":["Challenge","Points"],"id":"total_score"},
{"name":["Medals","Gold"],"id":"gm"},
{"name":["Medals","Silver"],"id":"sm"},
{"name":["Medals","Bronze"],"id":"bm"},
{"name":["Medals","Top 5"],"id":"T5"},
{"name":["Medals","Top 10"],"id":"T10"}
]

columns41 =[
{"name":["","Event"],"id":"eventid"},
{"name":["","Team"],"id":"team"},
{"name":["","Members"],"id":"members"},
{"name":["Modeling","Absolute"],"id":"model_abs"},
{"name":["Modeling","Relative"],"id":"model_rel"},
{"name":["Summary","Content"],"id":"exec_sum_con"},
{"name":["Summary","Format"],"id":"exec_sum_form"},
{"name":["Total","Points"],"id":"total_score"},
        ]


columns51 = [
{"name":["My Userid"],"id":"userid"},
{"name":["Team"],"id":"team"},
{"name":["Model Metric"],"id":"score"},
{"name":["Submitted"],"id":"time"},
]

col11 = [i['id'] for i in columns11]
col21 = [i['id'] for i in columns21]
col31 = [i['id'] for i in columns31]
col41 = [i['id'] for i in columns41]
col51 = [i['id'] for i in columns51]


