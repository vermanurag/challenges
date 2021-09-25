import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=basedir+"/../secret.env")

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BRAND = os.environ.get('BRAND')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATA_DIR = os.environ.get('DATA_DIR') or os.path.join(basedir, "data")
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'db/users.db')
    SQLALCHEMY_BINDS = {
        'my_data': os.environ.get('SQLALCHEMY_BIND_MY_DATA') or "sqlite:///" + os.path.join(basedir, "db/my_data.db")
    }
    IMG_FILE_DIR = os.environ.get('IMG_FILE_DIR') or os.path.join(basedir, "db/img")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    AUTHORITY_MS_TENANT = f"https://login.microsoftonline.com/{os.environ.get('TENANT_ID')}"
    AUTHORITY_MS_ORGS = f"https://login.microsoftonline.com/organizations/"
    AUTHORITY_MS_COMMONS = f"https://login.microsoftonline.com/commons/"
    REDIRECT_PATH = os.environ.get('REDIRECT_PATH') or '/getAToken'
    ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
    SCOPE = ["User.ReadBasic.All"]
    ADD_USER_AUTOMATICALLY=True
    AUTHORITY_MS=AUTHORITY_MS_ORGS
    AUTHORITY=AUTHORITY_MS_ORGS
    GOOGLE_SECRET_FILE = os.path.join(basedir,'../client_secret.json')
    GOOGLE_REDIRECT_PATH = os.environ.get('GOOGLE_REDIRECT_PATH','/getOAToken')
    GOOGLE_SCOPE = ['https://www.googleapis.com/auth/userinfo.email']
    LI_CLIENT_ID = os.environ.get('LI_CLIENT_ID')
    LI_SECRET = os.environ.get('LI_SECRET')
    LI_REDIRECT_PATH = os.environ.get('LI_REDIRECT_PATH','/getLiToken')
    LI_SCOPE = ['r_liteprofile r_emailaddress']
    BOOTSTRAP_BOOTSWATCH_THEME='cerulean'
    DASH_APP_1_URL='submit' #No spaces #All small
    DASH_APP_1_MENU_TEXT="Submit Results" #Can have spaces
    DASH_APP_1_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_2_URL='dashboard' #No spaces #All small
    DASH_APP_2_MENU_TEXT="Dashboard" #Can have spaces
    DASH_APP_2_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_3_URL='admin' #No spaces #All small
    DASH_APP_3_MENU_TEXT="Admin" #Can have spaces
    DASH_APP_3_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_4_URL='evaluation' #No spaces #All small
    DASH_APP_4_MENU_TEXT="Manual Evaluation" #Can have spaces
    DASH_APP_4_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_5_URL='v3' #No spaces #All small
    DASH_APP_5_MENU_TEXT="Capillus Numera(v3)" #Can have spaces
    DASH_APP_5_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_6_URL='v4' #No spaces #All small
    DASH_APP_6_MENU_TEXT="Capillus Numera(v4)" #Can have spaces
    DASH_APP_6_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_7_URL='v5' #No spaces #All small
    DASH_APP_7_MENU_TEXT="Capillus Numera(v5)" #Can have spaces
    DASH_APP_7_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_8_URL='placeholder' #No spaces #All small
    DASH_APP_8_MENU_TEXT="Placeholder App" #Can have spaces
    DASH_APP_8_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_9_URL='placeholder' #No spaces #All small
    DASH_APP_9_MENU_TEXT="Placeholder App" #Can have spaces
    DASH_APP_9_LOGIN_REQ=True # Whether login is required for this app
    DASH_APP_10_URL='placeholder' #No spaces #All small
    DASH_APP_10_MENU_TEXT="Placeholder App" #Can have spaces
    DASH_APP_10_LOGIN_REQ=True # Whether login is required for this app
    PREFIX=''
    PORT=''
    SERVER_URL=''
    PREFIX='/challenges' # only required if using prefix
    PORT=':8050' # only required if using prefix
    SERVER_URL='https://challenges.fnmathlogic.com' # only required if using prefix
    REDIRECT_URL = SERVER_URL+PORT+REDIRECT_PATH
    GOOGLE_REDIRECT_URL = SERVER_URL+PORT+GOOGLE_REDIRECT_PATH
    LI_REDIRECT_URL = SERVER_URL+PORT+LI_REDIRECT_PATH
    ACTIVE_DASH_APPS=[1,2,3,4]
    DEVELOPER_EMAIL='challenges@fnmathlogic.com'
