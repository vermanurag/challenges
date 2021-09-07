from flask import Flask, render_template, session, request, redirect, url_for, current_app
import msal
import dash_table
import pandas as pd
from app.main import bp
from app import db
from flask_login import current_user
from app.auth.models import Access

@bp.route("/")
@bp.route("/index")
@bp.route(current_app.config['PREFIX']+"/index")
def index():
    return redirect(current_app.config['SERVER_URL']+current_app.config['PREFIX']+"/home")


@bp.route("/home")
def home():
    if current_user.is_authenticated:
        access = Access.query.filter_by(email=current_user.email).all()
    else:
        access=[]
    return render_template('index.html',access=access)
