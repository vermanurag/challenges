import pandas as pd
import os
import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from app.dashapps.dash_app_4.base_data import *
from flask_login import current_user
from flask import flash

def register_callbacks(app):
    @app.callback(Output('questionid-dropdown','options'),
        [Input('eventid-dropdown','value')])
    def filter_brand(selected_event):
        print("filter_brand")
        print(selected_event)
        if (selected_event != None) & (selected_event != []):
            df11_filtered = df11[df11['eventid'] == selected_event]
            print(df11_filtered)
            return [{'label':i,'value' : i} for i in df11_filtered['questionid'].unique()]
        else:
            print("No event selected")
            return [{'label':'Select Event','value' : None}]

