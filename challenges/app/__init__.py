from flask import Flask, url_for, render_template

from config import Config

# extensions
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
lm = LoginManager()
lm.login_view = Config.SERVER_URL+Config.PREFIX+"/login"
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    # configuration
    app.config.from_object(config_class)

    # register extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    lm.init_app(app)

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    with app.app_context():
        # register blueprints
        from app.main import bp as bp_main
        app.register_blueprint(bp_main)
        from app.auth import bp as bp_auth
        app.register_blueprint(bp_auth)#, url_prefix='/auth')
        from app.dashapps import bp as bp_dashapps
        app.register_blueprint(bp_dashapps)

        # process dash apps
        from app.dashapps import _protect_dashviews
        for i in Config.ACTIVE_DASH_APPS:
            if i == 1:
                # dash app 1
                from app.dashapps.dash_app_1 import add_dash as ad1
                app = ad1(app, login_reg=Config.DASH_APP_1_LOGIN_REQ)
            if i == 2:
                ## dash app 2
                from app.dashapps.dash_app_2 import add_dash as ad2
                app = ad2(app, login_reg=Config.DASH_APP_2_LOGIN_REQ)
            if i == 3:
                # dash app 3
                from app.dashapps.dash_app_3 import add_dash as ad3
                app = ad3(app, login_reg=Config.DASH_APP_3_LOGIN_REQ)
            if i == 4:
                # dash app4
                from app.dashapps.dash_app_4 import add_dash as ad4
                app = ad4(app, login_reg=Config.DASH_APP_4_LOGIN_REQ)
            if i == 5:
                # dash app5
                from app.dashapps.dash_app_5 import add_dash as ad5
                app = ad5(app, login_reg=Config.DASH_APP_5_LOGIN_REQ)
            if i == 6:
                # dash app6
                from app.dashapps.dash_app_6 import add_dash as ad6
                app = ad6(app, login_reg=Config.DASH_APP_6_LOGIN_REQ)
            if i == 7:
                # dash app7
                from app.dashapps.dash_app_7 import add_dash as ad7
                app = ad7(app, login_reg=Config.DASH_APP_7_LOGIN_REQ)
            if i == 8:
                # dash app8
                from app.dashapps.dash_app_8 import add_dash as ad8
                app = ad8(app, login_reg=Config.DASH_APP_8_LOGIN_REQ)
        return app
