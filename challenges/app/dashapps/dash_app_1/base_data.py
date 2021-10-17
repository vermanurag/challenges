# base_data.py
import dash_html_components as html
from flask import current_app
from flask_login import current_user
import os
import base64
from datetime import datetime
from pathlib import Path
DATA_DIR = current_app.config['DATA_DIR']

import pandas as pd

def get_data(userid,creds = '/home/anuragverma/challenges/.gcp_key_competencyassessment.json'):
        from google.cloud import bigquery
        import os, json
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
        bq_client = bigquery.Client()
        query="""WITH view1 as
(select * from competencyassessment.assessment.event_questions where eventid in (select eventid from competencyassessment.assessment.event_users where userid = '{}'))
select eventid, q.questionid, type, file_type from view1 join competencyassessment.assessment.questions q on view1.questionid=q.questionid""".format(userid)
        query="""
WITH view1 as
(select * from competencyassessment.assessment.event_questions
   where eventid in
      (select e.eventid from competencyassessment.assessment.event_users u
           join competencyassessment.assessment.event e
           on u.eventid=e.eventid
           where userid = '{}'
           and e.active
           and e.event_end >= current_timestamp()
       )
)
select eventid, q.questionid, type, file_type from view1 join competencyassessment.assessment.questions q on view1.questionid=q.questionid
""".format(userid)
        query=query.replace('\n',' ')
        query=query.replace('  ',' ')
        query_job = bq_client.query(query)
        result = [dict(row) for row in query_job]
        return json.dumps(result)

def generate_random_filename():
    import random, string
    return "".join([random.choice(string.ascii_letters) for t in range(1,11)])

def save_file(contents, filename,DATA_DIR = DATA_DIR,creds = '/home/anuragverma/challenges/.gcp_key_competencyassessment.json'):
    from google.cloud import storage
    import os, base64, io
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds
    data = contents.encode("utf8").split(b";base64,")[1]
    #print(data)
    #print(contents)
    with open(os.path.join(DATA_DIR, filename), "wb") as fp:
        fp.write(base64.decodebytes(data))
    gcs_client = storage.Client()
    bucket= gcs_client.bucket('challenges-competencyassessment')
    blob = bucket.blob(filename)
    blob.upload_from_filename(os.path.join(DATA_DIR,filename))
    if blob.exists():
        return True
    else:
        return True


