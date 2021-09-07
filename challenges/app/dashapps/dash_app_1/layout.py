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
layout = html.Div("Placeholder for "+current_app.config['DASH_APP_1_MENU_TEXT'])

