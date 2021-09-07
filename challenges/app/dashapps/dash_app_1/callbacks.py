import pandas as pd
import os
import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from app.dashapps.dash_app_1.base_data import *
from flask_login import current_user
from flask import flash

def register_callbacks(app):
    @app.callback([Output('output-image-upload', 'children'),
                  Output('hidden-filename', 'children'),
                  Output('output-image-inference', 'hidden')],
                  [Input('upload-image', 'contents'),
                   Input('hidden-save-success','children')],
                  [State('upload-image', 'filename'),
                  State('upload-image', 'last_modified')])
    def update_output(list_of_contents,save_success, list_of_names, list_of_dates):
        ctx = dash.callback_context # get the context why the function is trigerred
        if ctx.triggered[0]['prop_id'] == 'hidden-save-success.children' and save_success == [True]:
            return ["Thanks. Your feedback has been saved.","",True]
        if list_of_contents is not None:
            filename = generate_random_filename()
            saved = save_image(list_of_contents[0], os.path.join(DATA_DIR,filename)) # Saves only the first file
            if saved:
              children = [
                parse_contents(c, n, d, filename) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
              return [children, filename,  False ]
            else:
              return ["Error uploading file", "", True ]
        else:
            raise PreventUpdate


    @app.callback([Output('model-inference', 'children'),
                  Output('output-image-feedback', 'hidden'),
                  Output('model-inference', 'hidden')],
                  [Input('process-image', 'n_clicks'),
                   Input('hidden-save-success','children'),
                   Input('hidden-filename', 'children')],
                  [State('upload-image','filename')])
    def get_model_inference(n_clicks, save_success, id, filename):
        ctx = dash.callback_context # get the context why the function is trigerred
        if (ctx.triggered[0]['prop_id'] == "hidden-filename.children") or (ctx.triggered[0]['prop_id'] == 'hidden-save-success.children' and save_success == [True]):
            return ["", True, True]
        elif ctx.triggered[0]['prop_id'] == "process-image.n_clicks":
            #TBD Code to call model and get inference
            model_inference = prediction(os.path.join(DATA_DIR,id))
            userid = current_user.email 
            result = derma_save(id,userid,filename[0],model_inference)
            #print(id, userid, filename, model_inference)
            #print(result)
            return [model_inference, False, False]
        else:
            raise PreventUpdate


    @app.callback([Output('hidden-save-success','children'),
                   Output('confirm-error','displayed')],
                  [Input('model-feedback-save', 'n_clicks')],
                  [State('hidden-filename', 'children'),
                  State('model-feedback-refid', 'value'),
                  State('model-feedback-dropdown', 'value'),
                  State('model-feedback-number', 'value'),
                  State('model-feedback-text', 'value')
                  ],
                  )
    def save_model_feedback(n_clicks, id, refid, flag, hc, comment):
        ctx = dash.callback_context # get the context why the function is trigerred
        if ctx.triggered[0]['prop_id'] == "model-feedback-save.n_clicks":
            userid = current_user.email 
            result = derma_save_feedback(id, refid, userid, flag, hc, comment)
            if result:
                return [[True], False]
            else:
                return [[False], True]
        else:
            raise PreventUpdate


