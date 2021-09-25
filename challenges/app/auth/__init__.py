from flask import Blueprint
import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for, current_app
import msal
import urllib
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

bp = Blueprint('auth', __name__, template_folder='templates')


def _build_msal_app(authority=None):
  return msal.ConfidentialClientApplication(
    current_app.config['CLIENT_ID'], authority=authority or current_app.config['AUTHORITY_MS'],
    client_credential=current_app.config['CLIENT_SECRET'])

def _build_msal_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("auth.authorized", _external=True) if current_app.config["PREFIX"]=='' else current_app.config['REDIRECT_URL'])

def _build_google_app():
  return google_auth_oauthlib.flow.Flow.from_client_secrets_file(
          current_app.config['GOOGLE_SECRET_FILE'],
        scopes=current_app.config['GOOGLE_SCOPE'])

def _build_google_auth_url(state=None):
    flow = _build_google_app()
    flow.redirect_uri=current_app.config['GOOGLE_REDIRECT_URL']
    return flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Include State for verification. Recommended as a bext practise
    state=state or str(uuid.uuid4()),
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true'
    )

def _build_li_auth_url(state=None):
    from flask import Request
    from werkzeug.test import create_environ
    params = {'client_id':current_app.config['LI_CLIENT_ID'],
            'response_type':'code',
            'redirect_uri':current_app.config['LI_REDIRECT_URL'],
            'state': state or str(uuid.uuid4()),
            'scope':current_app.config['LI_SCOPE']}
    environ = create_environ(base_url = 'https://www.linkedin.com/oauth/v2/authorization',query_string= params)
    request = Request(environ)
    return request.url

def _build_li_access_token(code=None):
    import requests
    params = {'client_id':current_app.config['LI_CLIENT_ID'],
            'grant_type':'authorization_code',
            'redirect_uri':current_app.config['LI_REDIRECT_URL'],
            'code': code,
            'client_secret':current_app.config['LI_SECRET']}
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    r = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data = params, headers = headers)
    print(r.text)
    return r

def _get_li_user_details(access_code=None):
    headers = {'Authorization' : 'Bearer '+ access_code}
    # Get name first
    r=requests.get("https://api.linkedin.com/v2/me",headers=headers)
    name = r.json().get('localizedFirstName') + " " + r.json().get('localizedLastName')
    # Now get email
    r=requests.get("https://api.linkedin.com/v2/clientAwareMemberHandles?q=members&projection=(elements*(primary,type,handle~))",headers=headers)
    email = r.json().get('elements')[0].get('handle~').get('emailAddress')
    if (email is not None) and email != '':
        return name, email
    else:
        return None, None

from app.auth import routes
