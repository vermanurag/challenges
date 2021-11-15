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
            #js_s= get_my_submission_data(userid)
            js_c= get_completed_event_data_local()
            #return [js_a, js_s,  js_c]
            return [js_a, js_c]
        except Exception as e:
            print("No User email or Error in accessing data")
            print(e)
            return [None, None]


    @app.callback([Output('eventid-dropdown','options'),
                   Output('eventid-dropdown','value')],
        [Input('hidden-data-active','data')],prevent_inital_call=True)
    def update_selection(js):
        print("updating active event view")
        import pandas as pd
        df11 = pd.read_json(js)
        event_list=list(df11['eventid'].unique())
        event_selected=event_list[0] if len(event_list) > 0 else None
        return [[{'label':i,'value' : i} for i in event_list], event_selected]

    @app.callback([Output('eventid-dropdown-c','options'),
                   Output('eventid-dropdown-c','value')],
        [Input('hidden-data-completed','data')])
    def update_selection_c(js):
        print("updating active event view")
        import pandas as pd
        df21 = pd.read_json(js)
        event_list=list(df21['eventid'].unique())
        event_selected=event_list[0] if len(event_list) > 0 else None
        return [[{'label':i,'value' : i} for i in event_list], event_selected]

    @app.callback([Output('eventid-dropdown-s','options'),
                   Output('eventid-dropdown-s','value')],
        [Input('hidden-data-submission','data')],prevent_initial_call=True)
    def update_selection_s(js):
        print("updating  submission view")
        import pandas as pd
        df51 = pd.read_json(js)
        event_list=list(df51['eventid'].unique())
        event_selected=event_list[0] if len(event_list) > 0 else None
        return [[{'label':i,'value' : i} for i in event_list], event_selected]


    @app.callback([Output('questionid-dropdown','options'),
                   Output('questionid-dropdown','value')],
        [Input('eventid-dropdown','value')],
        [State('hidden-data-active','data')],prevent_inital_call=True)
    def update_selection_q(eventid, js):
        print("updating active event view")
        import pandas as pd
        df11 = pd.read_json(js)
        question_list=list(df11[df11['eventid']==eventid]['questionid'].unique())
        question_selected=question_list[0] if len(question_list) > 0 else None
        return [[{'label':i,'value' : i} for i in question_list], question_selected]


    @app.callback([Output('questionid-dropdown-s','options'),
                   Output('questionid-dropdown-s','value')],
        [Input('eventid-dropdown-s','value')],
        [State('hidden-data-submission','data')],prevent_initial_call=True)
    def update_selection_qs(eventid, js):
        print("updating active event view")
        import pandas as pd
        df51 = pd.read_json(js)
        question_list=list(df51[df51['eventid']==eventid]['questionid'].unique())
        question_selected=question_list[0] if len(question_list) > 0 else None
        return [[{'label':i,'value' : i} for i in question_list], question_selected]


    @app.callback([Output('df11','data'),
                   Output('description','children')],
        [Input('questionid-dropdown','value')],
        [State('eventid-dropdown','value'),
        State('hidden-data-active','data')],prevent_inital_call=True)
    def update_selection_df11(questionid, eventid, js):
        print("updating active event view")
        import pandas as pd
        df11 = pd.read_json(js)
        df=df11[(df11['eventid']==eventid) & (df11['questionid']==questionid)].sort_values("rank")
        desc=list(df['description'].unique())[0]
        return [df[col11].to_dict('records'), desc]


    @app.callback([Output('df21','data'),
                   Output('description-c','children'),
                   ],
        [Input('eventid-dropdown-c','value'),
        Input('hidden-data-completed','data')],prevent_initial_call=True)
    def update_selection_df21(eventid,  js):
        print("updating  completed event view")
        import pandas as pd
        df = pd.read_json(js)
        df21=df[(df['eventid']==eventid)].sort_values("rank")
        desc=list(df21['description'].unique())[0]
        return [df21[col21].to_dict('records'), desc]


    @app.callback([Output('df31','data'),
                   Output('df41','data')],
        [ Input('hidden-data-completed','data')],prevent_initial_call=True)
    def update_selection_df31(js):
        print("updating  completed event views")
        import pandas as pd
        df = pd.read_json(js)
        df2=df[['members','rank','total_score']].copy()
        df31= overall(df_in=df2,userid=current_user.email)
        df41 = df[df['members'].str.contains(current_user.email)].sort_values('total_score')
        return [df31[col31].to_dict('records'), df41[col41].to_dict('records')]


    @app.callback([Output('df51','data'),
                   Output('description-s','children')],
        [Input('eventid-dropdown-s','value'),
        Input('questionid-dropdown-s','value'),
        Input('hidden-data-submission','data')],prevent_inital_call=True)
    def update_selection_df51(eventid, questionid, js):
        if questionid is None:
            return [None,""]
        else:
            print("updating submission df view")
            import pandas as pd
            df = pd.read_json(js)
            df51=df[(df['eventid']==eventid) & (df['questionid']==questionid)].sort_values("time",ascending=False)
            desc=list(df51['description'].unique())[0]
            return [df51[col51].to_dict('records'), desc]


    @app.callback([Output('hidden-data-submission','data')],
        [Input('tabs','value')],
        State('hidden-data-submission','data'),prevent_initial_call=True)
    def get_base_data(tab, js_s):
        print("refreshing submission data")
        if tab != 'tab5' or js_s is not None:
            raise PreventUpdate
        try:
            userid = current_user.email
            #print(userid)
            js_s= get_my_submission_data(userid)
            return [js_s]
        except Exception as e:
            print("No User email or Error in accessing data")
            print(e)
            return [None]


