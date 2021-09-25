import dash_html_components as html
from flask import Flask, render_template, session, request, redirect, url_for, current_app
import dash,dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dashapps.dash_app_3.base_styles import *
from app.dashapps.dash_app_3.base_data import *
import dash_pivottable
#layout = html.Div("Placeholder for "+current_app.config['DASH_APP_3_MENU_TEXT'])
layout = html.Div([
html.Br(),
dbc.Row(children = [
	dbc.Col(children=[],width=1),
	dbc.Col(children=[
		dbc.Row(children =[html.Div('Event', className='btn btn-primary btn-lg', style = {'width': '30%'}),
			dcc.Dropdown(id='eventid-dropdown', className = "btn btn-lg", style = {'width': '200px'}, options=[{'label': i, 'value': i} for i in EVENT_LIST])]),
		dbc.Row(children=[html.Div('Question', className='btn btn-primary btn-lg',style = {'width': '30%'}),
			dcc.Dropdown(id='questionid-dropdown', className = "btn btn-lg" , style = {'width': '200px'}, options = [] )])
	], width = 4),
	dbc.Col(children = [
		dbc.Row(dcc.Input(id='solution-value', type ='text', placeholder ='Your Solution Value', size =24 )),
		dbc.Row(dcc.Input(id='bucket-name', type ='text', placeholder ='Your Bucket Name', size=24 )),
		dbc.Row(dcc.Upload(id='solution-file',children=html.Div(['Drag and Drop or ', html.A('Select Files')],className = 'btn btn-primary nav-link active'),
	        multiple=False))
	], width = 4),
	dbc.Col(html.Button("Submit",id='submit', n_clicks=0, className = 'btn btn-primary btn-lg'),width=3),
])
])


