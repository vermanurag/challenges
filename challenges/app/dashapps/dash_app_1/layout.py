import dash_html_components as html
from flask import Flask, render_template, session, request, redirect, url_for, current_app
import dash,dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dashapps.dash_app_1.base_styles import *
from app.dashapps.dash_app_1.base_data import *
import dash_pivottable
layout = html.Div([
html.Br(),
dbc.Row(children = [
	dbc.Col(children=[],width=1),
	dbc.Col(children=[
		dbc.Row(children =[html.Div('Event', className='btn btn-primary btn-lg', style = {'width': '30%'}),
			dcc.Dropdown(id='eventid-dropdown', className = "btn btn-lg", style = {'width': '400px'}, options=[])]),
		dbc.Row(children=[html.Div('Question', className='btn btn-primary btn-lg',style = {'width': '30%'}),
			dcc.Dropdown(id='questionid-dropdown', className = "btn" , style = {'width': '400px'}, options = [] )])
	], width = 7),
	dbc.Col(children = [
		dbc.Row(html.Div(id='solution-value-wrapper',hidden=True,children=[dcc.Input(id='solution-value', type ='text', placeholder ='Your Solution Value')])),
		dbc.Row(html.Div(id='bucket-name-wrapper',hidden=True,children=[dcc.Input(id='bucket-name', type ='text', placeholder ='Your Bucket Name')])),
		dbc.Row(html.Div(id='solution-file-wrapper', hidden=True, children=[dcc.Upload(id='solution-file',accept='.csv',children=html.Div(['Drag and Drop or ', html.A('Select Files')],className = 'btn btn-primary nav-link active'),
			multiple=False),html.Div(id='uploaded-file',style={'color': 'gray', 'fontSize': 10})]))
	], width = 2),
	dbc.Col(children = [html.Button("Submit*",id='submit', n_clicks=0, className = 'btn btn-primary btn-lg'),
		html.Br(),
		html.Button("Refresh",id='refresh', n_clicks=0, className = 'btn btn-primary btn-lg', hidden=True)],width = 2),
]),
html.Br(),
dbc.Row(children=[dbc.Col(children=[],width=1), dbc.Col(children=[html.Div(id='submission-message',children = "",className = "btn btn-outline-primary", style = button ,hidden = True)])]),
dcc.Store(id='hidden-data'),
dcc.Store(id='hidden-question-type'),
dcc.Store(id='hidden-file-name'),
dbc.Row(children = [
	dbc.Col(children=[],width=1),html.Div(id='wait-message',children="* Allow upto 10 seconds for submission to be recorded",style={'color': 'gray', 'fontSize': 10}),
     ])
])

