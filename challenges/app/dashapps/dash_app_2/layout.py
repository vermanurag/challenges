#layout.py
import dash_html_components as html
from flask import Flask, render_template, session, request, redirect, url_for, current_app
import dash,dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dashapps.dash_app_2.base_styles import *
from app.dashapps.dash_app_2.base_data import *
import dash_pivottable
#layout = html.Div("Placeholder for "+current_app.config['DASH_APP_2_MENU_TEXT'])
layout = dbc.Col(html.Div(children=[html.Br(),
html.Div(html.H4(id='dashboard-heading',style={'width':'100%','margin':'auto'})),
html.Button("Refresh",id='refresh', n_clicks=0, className = 'btn btn-primary btn-lg', hidden=True),
dcc.Store(id='hidden-data'),
dcc.Tabs(id='tabs', value='tab3', children=[
                dcc.Tab(label='Overall', id='tab1', value='tab1',disabled=True),
                dcc.Tab(label='Active Events', id='tab2', value='tab2', disabled = True),
                dcc.Tab(label='GCP Academy', id='tab3', value='tab3'),
                dcc.Tab(label='DS Challenges', id='tab4', value='tab4', disabled = True),
                dcc.Tab(label='AWS Academy', id='tab5', value='tab5', disabled = True),
                dcc.Tab(label='All Submissions', id='tab6', value='tab6', disabled = True),
                ]),
                html.Div(id='tab-content-1',children=[
                    dash_table.DataTable(id='df11',css=dashtable_css,columns=columns11,data=df11[col11].to_dict('records'),editable=True, row_selectable='multi', merge_duplicate_headers=True, sort_action = 'native' ,style_header=style_header, style_data_conditional=style_data_conditional)]),
                html.Div(id='tab-content-2',children=[
                    dash_table.DataTable(id='df21',css=dashtable_css,columns=columns21,data=df21[col21].to_dict('records'),editable=True, merge_duplicate_headers=True,  sort_action = 'native' ,style_header=style_header, style_data_conditional=style_data_conditional)]),
                html.Div(id='tab-content-3',children=[
                    dash_table.DataTable(id='df31',css=dashtable_css,columns=columns31, merge_duplicate_headers=True, style_header=style_header, sort_action = 'native',filter_action="native" , style_data_conditional=style_data_conditional)]),
                html.Div(id='tab-content-4',children=[
                    dash_table.DataTable(id='df41',css=dashtable_css,columns=columns41,data=df41[col41].to_dict('records'), merge_duplicate_headers=True, style_header=style_header, sort_action = 'native' , style_data_conditional=style_data_conditional)]),
                html.Div(id='tab-content-5',children=[
                    dash_table.DataTable(id='df51',css=dashtable_css,columns=columns51,data=df51[col51].to_dict('records'), merge_duplicate_headers=True, style_header=style_header, sort_action = 'native' , style_data_conditional=style_data_conditional)]),
                html.Div(id='tab-content-6',children=[
                    dash_table.DataTable(id='df61',css=dashtable_css,columns=columns61,data=df61[col61].to_dict('records'), merge_duplicate_headers=True, style_header=style_header, sort_action = 'native' , style_data_conditional=style_data_conditional)]),
                    ]))

