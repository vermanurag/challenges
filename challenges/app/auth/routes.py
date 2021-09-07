import uuid
import requests
from flask import Flask, redirect, url_for, render_template, flash, current_app, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth import _build_msal_auth_url, _build_msal_app, _build_google_auth_url, _build_google_app
from app.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests as R


@bp.route('/logout')
@login_required
def logout():
    source = current_user.source
    logout_user()
    if source == 'MS':
        return redirect(  # Also logout from your tenant's web session
         current_app.config['AUTHORITY'] + "/oauth2/v2.0/logout" +
         "?post_logout_redirect_uri=" + url_for("main.index", _external=True))
    elif source == 'GOOG':
        return redirect(url_for("main.index"))
    else:
        return redirect(url_for("main.index"))

@bp.route('/login_warning')
def login_warning():
    return redirect(current_app.config['PREFIX']+url_for('auth.login'))


@bp.route('/login', methods=['GET'])
def login():
    next_url = request.args.get('next')
    if not current_user.is_anonymous:
        flash(f'Logged in as {current_user.name}', 'success')
        return redirect(current_app.config['PREFIX']+(next_url or url_for('main.index')))
    else:
        session["state"] = str(uuid.uuid4())
        auth_url = _build_msal_auth_url(scopes=current_app.config['SCOPE'], state=session["state"])
        google_auth_url, _ = _build_google_auth_url(state=session["state"])
        return render_template("auth/login.html", auth_url=auth_url,google_auth_url=google_auth_url)

@bp.route(current_app.config['REDIRECT_PATH'], methods=['GET'])
def authorized():
    next_url = request.args.get('next')

    if request.args.get('state') != session.get("state"):
        return redirect(current_app.config['PREFIX']+url_for('main.index'))  # No-OP. Goes back to Index page

    if not current_user.is_anonymous:
        return redirect(next_url or url_for('main.index'))

    if request.args.get('code'):
        result = _build_msal_app().acquire_token_by_authorization_code(
            request.args['code'],
            scopes=current_app.config['SCOPE'],  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("auth.authorized", _external=True))
        if "error" in result:
            flash('Authentication failed', 'danger')
            return redirect(url_for('auth.login'))

        claims = result.get("id_token_claims")
        name = claims['name']
        email = claims['preferred_username']
        if name is None or email is None:
            flash('Authentication failed.')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(email=email).first()
        useremail = User.query.filter_by(email=email).first()

        if current_app.config['ADD_USER_AUTOMATICALLY'] and not useremail:
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.commit()
        else:
            if not user and useremail:
                useremail.name=name
                db.session.commit()
            elif not useremail:
                flash('Authenticated User does not have Access to system.')
                flash('Get in touch with System Administrator for Access.')
                return redirect(url_for('auth.logout'))

        logged_in = login_user(user, remember=True, force=True)

    else:
        redirect(current_app.config['PREFIX']+url_for('auth.login'))

    return redirect(next_url or url_for('main.index'))

@bp.route(current_app.config['GOOGLE_REDIRECT_PATH'], methods=['GET'])
def google_authorized():
    next_url = request.args.get('next')

    if request.args.get('state') != session.get("state"):
        return redirect(current_app.config['PREFIX']+url_for('main.index'))  # No-OP. Goes back to Index page

    if not current_user.is_anonymous:
        return redirect(next_url or url_for('main.index'))

    if request.args.get('code'):
        authorization_response = request.url
        #result = _build_google_app().fetch_token(authorization_response=authorization_response)
        flow = _build_google_app()
        flow.redirect_uri=url_for("auth.google_authorized", _external=True)
        try:
            result = flow.fetch_token(authorization_response=authorization_response)
            claims_token = result.get("id_token")
            r= R.Request()
            id_info = id_token.verify_oauth2_token(claims_token,r)
            print(id_info)
        except:
            flash('Authentication failed', 'danger')
            return redirect(url_for('auth.login'))
        name = id_info.get('name')
        email = id_info.get('email')
        if name is None and email is not None:
            name = email
        if name is None or email is None:
            flash('Authentication failed.')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(email=email).first()
        useremail = User.query.filter_by(email=email).first()

        if current_app.config['ADD_USER_AUTOMATICALLY'] and not useremail:
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.commit()
        else:
            if not user and useremail:
                useremail.name=name
                db.session.commit()
            elif not useremail:
                flash('Authenticated User does not have Access to system.')
                flash('Get in touch with System Administrator for Access.')
                return redirect(url_for('auth.logout'))

        logged_in = login_user(user, remember=True, force=True)

    else:
        redirect(current_app.config['PREFIX']+url_for('auth.login'))

    return redirect(next_url or url_for('main.index'))

