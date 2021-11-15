#layout.py
import dash_html_components as html
from flask import Flask, render_template, session, request, redirect, url_for, current_app
import dash,dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dashapps.dash_app_4.base_styles import *
from app.dashapps.dash_app_4.base_data import *
import dash_pivottable
#layout = html.Div("Placeholder for "+current_app.config['DASH_APP_2_MENU_TEXT'])
layout = dbc.Col(html.Div(children=[html.Br(),
html.Div(html.H4(id='dashboard-heading',style={'width':'100%','margin':'auto'})),
html.Button("Refresh",id='refresh', n_clicks=0, className = 'btn btn-primary btn-lg', hidden=True),
dcc.Store(id='hidden-manual-evaluation'),
dcc.Store(id='hidden-file_link'),
html.Br(),
html.Div(id='tab-content-1',
children=[
       html.Div(children = [dbc.Row(children=[
          dbc.Col(children=[html.Div('Event', className='btn btn-primary btn-lg', style = {'width': '100%'}),
          dcc.Dropdown(id='eventid-dropdown', className = "btn btn-lg", style = {'width': '400px'}, options=[{'label': i, 'value': i} for i in EVENTLIST],value=EVENTLIST[0])], width=6),
          dbc.Col(children=[html.Div('Question', className='btn btn-primary btn-lg',style = {'width': '100%'}),
          dcc.Dropdown(id='questionid-dropdown', className = "btn" , style = {'width': '400px'}, options = [] )], width=6)]),
          dbc.Row(html.Button(id="description", className="btn btn-primary btn-lg", n_clicks=0, style = {'width':'100%'})),
          html.Br(),
          dcc.Input(id='content'),dcc.Input(id='format'),
          html.Div(
              html.Iframe(
                  src="https://storage.cloud.google.com/challenges-exec-summary/783b0bed-7c51-40ac-90f8-38434d51c40bmonica.marmit%40fnmathlogic.comSDxRueeASs.pdf",
                  style={"width":"100%","height":"600px"}
        ))
          ])
          ]),
                    ]))

