import pandas as pd
import os
import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from app.dashapps.dash_app_4.base_data import *
from flask_login import current_user
from flask import flash

def register_callbacks(app):

    @app.callback([Output('questionid-dropdown','options'),
                   Output('questionid-dropdown','value')],
        [Input('eventid-dropdown','value'),
        ],prevent_inital_call=True)
    def update_selection_q(eventid):
        question_list=[MANUAL_QUESTIONID.get(eventid)]
        question_selected=question_list[0] if len(question_list) > 0 else None
        return [[{'label':i,'value' : i} for i in question_list], question_selected]


    @app.callback([ Output('description','children')],
        [ Input('questionid-dropdown','value'),
        ],prevent_inital_call=True)
    def update_selection_questionid(questionid):
        print("updating active event view")
        import pandas as pd
        desc = QUESTIONID_DESC.get(questionid)
        return [ desc]


