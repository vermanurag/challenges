# callback.py
import pandas as pd
import os, json, requests
import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from app.dashapps.dash_app_1.base_data import *
from flask_login import current_user
from flask import flash

def register_callbacks(app):
    @app.callback(Output('questionid-dropdown','options'),
        [Input('eventid-dropdown','value'),
         Input('hidden-data','data')])
    def filter_question(selected_event, js):
        #print("filter_brand")
        #print(selected_event)
        if (selected_event != None) & (selected_event != []):
            question_list = list(set([row['questionid'] for row in json.loads(js) if row['eventid'] == selected_event]))
            return [{'label':i,'value' : i} for i in question_list]
        else:
            print("No event selected")
            return []

    @app.callback([Output('hidden-data','data'),
        Output('eventid-dropdown','options')],
        [Input('refresh','n_clicks')])
    def get_base_data(n_clicks):
        print("refreshing data")
        try:
            userid = current_user.email
            #print(userid)
            js = get_data(userid)
            event_list = list(set([row['eventid'] for row in json.loads(js)]))
            return [js,[{'label':i,'value' : i} for i in event_list]]
        except Exception as e:
            print("No User email or Error in accessing data")
            print(e)

    @app.callback([Output('solution-value-wrapper','hidden'),
        Output('bucket-name-wrapper','hidden'),
        Output('solution-file-wrapper','hidden'),
        Output('solution-file','accept'),
        Output('hidden-question-type','data')],
        [Input('questionid-dropdown','value'),
        Input('hidden-data','data')])
    def filter_output_param(selected_question,js):
        if (selected_question != None) & (selected_question != []):
            question_type = [row['type'] for row in json.loads(js) if row['questionid'] == selected_question][0]
            file_type = [row['file_type'] for row in json.loads(js) if row['questionid'] == selected_question][0]
            if question_type in [0,1]:
                return [False, True, True, "","solution_value"]
            elif question_type in [3,5]:
                return [True, False, True, "","bucket_name"]
            else:
                if file_type in ('.csv','application/pdf', 'application/json', 'text/plain', 'application/xml','image/png', 'image/jpeg', 'image/gif', 'image/jpg'):
                    print(file_type)
                    return [True, True, False, file_type,"solution_file"]
                else:
                    return [True, True, False, ".csv", "soluton_file"]
            return 
        else:
            print("No question selected")
            return [True, True, True, 'text/csv',"None"]

    @app.callback([Output('submission-message','children'),
        Output('submission-message','hidden')],
        [Input('submit','n_clicks'),
        Input('eventid-dropdown','value'),
        Input('questionid-dropdown','value'),
        Input('hidden-question-type','data'),
        Input('solution-value','value'),
        Input('bucket-name','value'),
        Input('hidden-file-name','data')
         ])
    def submit_response(n_clicks, eventid, questionid, qtype , solution_value, bucket_name, solution_file):
        #print("submitting data")
        ctx = dash.callback_context # get the context why the function is trigerred
        if ctx.triggered[0]['prop_id'] != "submit.n_clicks":
            raise PreventUpdate
        skip= False
        base_url='https://us-central1-competencyassessment.cloudfunctions.net/evaluate'
        userid=current_user.email
        params={'eventid':eventid, 'userid':userid,'questionid':questionid }
        if qtype == 'solution_value':
            params['solution_value'] = solution_value
        elif qtype == 'bucket_name':
            params['bucket_name'] = bucket_name
        elif qtype == 'solution_file':
            params['solution_file'] = "gs://challenges-competencyassessment/"+solution_file
        else:
            message = "Invalid Question Type or Question Id not selected"
            skip = True
        print(params)
        if skip:
            pass
        else:
            r = requests.get(base_url,params=params)
            message = r.text
        return(message, False)

    @app.callback([Output('hidden-file-name','data'),
    	Output('uploaded-file','children'),
    	Output('uploaded-file','hidden')],
        [Input('solution-file','contents'),
         Input('solution-file','filename')])
    def save_uploaded_file(contents, orig_file_name):
        print("Uploading File")
        if contents is not None:
            filename = generate_random_filename()
            saved = save_file(contents, filename) # Saves only the first file
            if saved:
                print("file saved")
                return [filename,orig_file_name,False]
            else:
                print("error saving file to GCS")
                return ["","Error processing.",False]
        else:
            raise PreventUpdate


