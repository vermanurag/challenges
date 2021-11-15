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
dcc.Store(id='hidden-data-active'),
dcc.Store(id='hidden-data-completed'),
dcc.Store(id='hidden-data-submission'),
dcc.Tabs(id='tabs', value='tab1', children=[
                dcc.Tab(label='Live Challenge', id='tab1', value='tab1',disabled=False),
                dcc.Tab(label='Completed Challenges', id='tab2', value='tab2', disabled = False),
                dcc.Tab(label='Overall Standing', id='tab3', value='tab3', disabled=False),
                dcc.Tab(label='My Challenge Points', id='tab4', value='tab4', disabled = False),
                dcc.Tab(label='My Submissions', id='tab5', value='tab5', disabled = False),
                ]),
html.Br(),
html.Div(id='tab-content-1',
children=[
       html.Div(children = [dbc.Row(children=[
          dbc.Col(children=[html.Div('Event', className='btn btn-primary btn-lg', style = {'width': '100%'}),
          dcc.Dropdown(id='eventid-dropdown', className = "btn btn-lg", style = {'width': '400px'}, options=[])], width=6),
          dbc.Col(children=[html.Div('Question', className='btn btn-primary btn-lg',style = {'width': '100%'}),
          dcc.Dropdown(id='questionid-dropdown', className = "btn" , style = {'width': '400px'}, options = [] )], width=6)]),
          dbc.Row(html.Button(id="description", className="btn btn-primary btn-lg", n_clicks=0, style = {'width':'100%'})),
          html.Br(),
          html.Div(children=dash_table.DataTable(id='df11',css=dashtable_css,columns=columns11,data=None, merge_duplicate_headers=True, sort_action = 'native', filter_action='native' ,style_header=style_header, style_data_conditional=style_data_conditional))
          ])
          ]),
html.Div(id='tab-content-2',
children=[
       html.Div(children = [dbc.Row(children=[
          dbc.Col(children=[html.Div('Event', className='btn btn-primary btn-lg', style = {'width': '100%'}),
          dcc.Dropdown(id='eventid-dropdown-c', className = "btn btn-lg", style = {'width': '400px'}, options=[])], width=12)]),
          dbc.Row(html.Button(id="description-c", className="btn btn-primary btn-lg", n_clicks=0, style = {'width':'100%'})),
          html.Br(),
          html.Div(children=dash_table.DataTable(id='df21',css=dashtable_css,columns=columns21,data=None, merge_duplicate_headers=True, sort_action = 'native', filter_action='native',style_header=style_header, style_data_conditional=style_data_conditional))
          ])
          ]),
                html.Div(id='tab-content-3',children=[
                    dash_table.DataTable(id='df31',css=dashtable_css,columns=columns31, merge_duplicate_headers=True, style_header=style_header, filter_action='native',sort_action = 'native', style_data_conditional=style_data_conditional)]),
                html.Div(id='tab-content-4',children=[
                    dash_table.DataTable(id='df41',css=dashtable_css,columns=columns41,data=None, merge_duplicate_headers=True, style_header=style_header, sort_action = 'native' , style_data_conditional=style_data_conditional)]),
html.Div(id='tab-content-5',
children=[
       html.Div(children = [dbc.Row(children=[
          dbc.Col(children=[html.Div('Event', className='btn btn-primary btn-lg', style = {'width': '100%'}),
          dcc.Dropdown(id='eventid-dropdown-s', className = "btn btn-lg", style = {'width': '400px'}, options=[])], width=6),
          dbc.Col(children=[html.Div('Question', className='btn btn-primary btn-lg',style = {'width': '100%'}),
          dcc.Dropdown(id='questionid-dropdown-s', className = "btn" , style = {'width': '400px'}, options = [] )], width=6)]),
          dbc.Row(children=[html.Button(id="description-s", className="btn btn-primary btn-lg", n_clicks=0, style = {'width':'100%'}),
              ]),
          html.Br(),
          html.Div(children=dash_table.DataTable(id='df51',css=dashtable_css,columns=columns51,data=None, merge_duplicate_headers=True, sort_action = 'native', filter_action='native' ,style_header=style_header, style_data_conditional=style_data_conditional))
          ])
          ]),
                html.Div(id='tab-content-6',children=[
                    ])]))

