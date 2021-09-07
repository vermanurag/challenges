from flask import Flask, render_template, session, request, redirect, url_for, current_app
from flask_login import current_user, login_required
from app.auth.models import Access
from app.dashapps import bp

if (1 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_1 as dash_app_1_obj
    @bp.route("/"+current_app.config['DASH_APP_1_URL'])
    @login_required
    def dash_app_1():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_1').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_1_obj.URL_BASE, min_height=dash_app_1_obj.MIN_HEIGHT)

if (2 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_2 as dash_app_2_obj
    @bp.route("/"+current_app.config['DASH_APP_2_URL'])
    @login_required
    def dash_app_2():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_2').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_2_obj.URL_BASE, min_height=dash_app_2_obj.MIN_HEIGHT)

if (3 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_3 as dash_app_3_obj
    @bp.route("/"+current_app.config['DASH_APP_3_URL'])
    @login_required
    def dash_app_3():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_3').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_3_obj.URL_BASE, min_height=dash_app_3_obj.MIN_HEIGHT)

if (4 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_4 as dash_app_4_obj
    @bp.route("/"+current_app.config['DASH_APP_4_URL'])
    @login_required
    def dash_app_4():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_4').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_4_obj.URL_BASE, min_height=dash_app_4_obj.MIN_HEIGHT)

if (5 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_5 as dash_app_5_obj
    @bp.route("/"+current_app.config['DASH_APP_5_URL'])
    @login_required
    def dash_app_5():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_5').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_5_obj.URL_BASE, min_height=dash_app_5_obj.MIN_HEIGHT)

if (6 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_6 as dash_app_6_obj
    @bp.route("/"+current_app.config['DASH_APP_6_URL'])
    @login_required
    def dash_app_6():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_6').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_6_obj.URL_BASE, min_height=dash_app_6_obj.MIN_HEIGHT)

if (7 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_7 as dash_app_7_obj
    @bp.route("/"+current_app.config['DASH_APP_7_URL'])
    @login_required
    def dash_app_7():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_7').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_7_obj.URL_BASE, min_height=dash_app_7_obj.MIN_HEIGHT)

if (8 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_8 as dash_app_8_obj
    @bp.route("/"+current_app.config['DASH_APP_3_URL'])
    @login_required
    def dash_app_8():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_8').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_8_obj.URL_BASE, min_height=dash_app_8_obj.MIN_HEIGHT)

if (9 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_9 as dash_app_9_obj
    @bp.route("/"+current_app.config['DASH_APP_9_URL'])
    @login_required
    def dash_app_9():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_9').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_9_obj.URL_BASE, min_height=dash_app_9_obj.MIN_HEIGHT)

if (10 in current_app.config['ACTIVE_DASH_APPS']):
    from app.dashapps import dash_app_10 as dash_app_10_obj
    @bp.route("/"+current_app.config['DASH_APP_10_URL'])
    @login_required
    def dash_app_10():
        access = Access.query.filter_by(email=current_user.email,app_id='dash_app_10').first_or_404(description='User {} does not have access to this app'.format(current_user.name))
        return render_template('dashapps/dash_app.html', dash_url=dash_app_10_obj.URL_BASE, min_height=dash_app_10_obj.MIN_HEIGHT)
