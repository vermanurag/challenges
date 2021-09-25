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
layout = html.Div(children=[
    html.Br(),
    dash_table.DataTable(
    id='overall_table',
    css=dashtable_css,merge_duplicate_headers=True, style_header=style_header, style_data_conditional=style_data_conditional,
    columns=columns_overall,
    data=df_overall.to_dict('records'),
)])
