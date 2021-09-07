import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app.dashapps import _protect_dashviews
import pandas as pd
import dash_table
from dash.dependencies import Input, Output, State
from flask import Flask, render_template, session, request, redirect, url_for, current_app
from app.dashapps.dash_app_1.layout import layout
from app.dashapps.dash_app_1.callbacks import register_callbacks

APP_ID = current_app.config['DASH_APP_1_URL']
URL_BASE = '/dummypath/'+APP_ID+'/'
MIN_HEIGHT = 500
try:
    THEME=current_app.config['BOOTSTRAP_BOOTSWATCH_THEME'].upper()
    es="import dash_bootstrap_components as dbc; external_stylesheets = [dbc.themes.{}]".format(THEME)
    exec(es)
except:
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
    ]

def add_dash(server, login_reg=True):
    app = dash.Dash(
        server=server,
        url_base_pathname=URL_BASE,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
    )

    if login_reg:
        _protect_dashviews(app)

    #app.layout = html.Div("Placeholder for "+current_app.config['DASH_APP_1_MENU_TEXT'])
    app.layout = layout

    #@app.callback(Output('segment-dropdown','options'),[Input('brand-dropdown','value'),Input('category-dropdown','value')])
    register_callbacks(app)
  
    return server

if __name__ == '__main__':
    from flask import Flask, render_template
    from flask_bootstrap import Bootstrap

    bootstrap = Bootstrap()
    app = Flask(__name__)
    bootstrap.init_app(app)

    # inject Dash
    app = add_dash(app, login_reg=False)

    @app.route(URL_BASE+'debug')
    def dash_app():
        return render_template('dashapps/dash_app_debug.html', dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 7001
    print(f'http://localhost:{app_port}{URL_BASE}/debug')
    app.run(debug=True)#, port=app_port)
