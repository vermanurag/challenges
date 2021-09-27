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

    @app.callback([Output('hidden-data','data')],
        [Input('refresh','n_clicks')])
    def get_base_data(n_clicks):
        print("refreshing data")
        try:
            userid = current_user.email
            #print(userid)
            js = get_gcp_academy_data(userid)
            return [js]
        except Exception as e:
            print("No User email or Error in accessing data")
            print(e)

    @app.callback([Output('df31','data')],
        [Input('hidden-data','data')])
    def update_df31(js):
        print("updating df31")
        import pandas as pd
        df31 = pd.read_json(js)
        df31 = df31[df31['userid'] == current_user.email]
        return [df31.to_dict('records')]

