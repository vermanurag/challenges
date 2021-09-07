import sys, os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,basedir+"/challenges")
import app
application = app.create_app()
