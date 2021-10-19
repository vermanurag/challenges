import pandas as pd
import os
import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from app.dashapps.dash_app_2.base_data import *
from flask_login import current_user
from flask import flash

def register_callbacks(app):
    @app.callback([Output('tab-content-1', 'hidden'), Output('tab-content-2', 'hidden'), Output('tab-content-3', 'hidden'), Output('tab-content-4', 'hidden'), Output('tab-content-5', 'hidden'), Output('tab-content-6', 'hidden')],
                  [Input('tabs', 'value')])
    def render_content_1(tab):
        print("render_content ",tab)
        if tab == 'tab1':
            return False, True, True, True, True, True
        elif tab == 'tab2':
            return True, False, True, True, True, True
        elif tab == 'tab3':
            return True, True, False, True, True, True
        elif tab == 'tab4':
            return True, True, True, False, True, True
        elif tab == 'tab5':
            return True, True, True, True, False, True
        elif tab == 'tab6':
            return True, True, True, True, True, False
        else:
            return False, True, True, True, True, True

    @app.callback([Output('hidden-data-active','data'),
        Output('hidden-data-completed','data')],
        [Input('refresh','n_clicks')])
    def get_base_data(n_clicks):
        print("refreshing data")
        try:
            userid = current_user.email
            #print(userid)
            js_a= get_active_event_data(userid)
            js_c= get_completed_event_data(userid)
            return [js_a, js_c]
        except Exception as e:
            print("No User email or Error in accessing data")
            print(e)
            return [None, None]


    @app.callback([Output('eventid-dropdown','options'),
                   Output('eventid-dropdown','value')],
        [Input('hidden-data-active','data')])
    def update_selection(js):
        print("updating active event view")
        import pandas as pd
        df11 = pd.read_json(js)
        event_list=list(df11['eventid'].unique())
        event_selected=event_list[0] if len(event_list) > 0 else None
        return [[{'label':i,'value' : i} for i in event_list], event_selected]

    @app.callback([Output('questionid-dropdown','options'),
                   Output('questionid-dropdown','value')],
        [Input('eventid-dropdown','value'),
        Input('hidden-data-active','data')])
    def update_selection_q(eventid, js):
        print("updating active event view")
        import pandas as pd
        df11 = pd.read_json(js)
        question_list=list(df11[df11['eventid']==eventid]['questionid'].unique())
        question_selected=question_list[0] if len(question_list) > 0 else None
        return [[{'label':i,'value' : i} for i in question_list], question_selected]

    @app.callback([Output('df11','data'),
                   Output('description','children')],
        [Input('eventid-dropdown','value'),
        Input('questionid-dropdown','value'),
        Input('hidden-data-active','data')])
    def update_selection_q(eventid, questionid, js):
        print("updating active event view")
        import pandas as pd
        df11 = pd.read_json(js)
        df=df11[df11['eventid']==eventid][df11['questionid']==questionid]
        desc=df['description'][0]
        return [df[col11].to_dict('records'), desc]

