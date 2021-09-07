bind = "0.0.0.0:8050"
workers = 8
keyfile = '/etc/letsencrypt/live/challenges.fnmathlogic.com/privkey.pem'
certfile = '/etc/letsencrypt/live/challenges.fnmathlogic.com/fullchain.pem'
accesslog = '/var/log/gunicorn/gunicorn_access_ch.log'
errorlog = '/var/log/gunicorn/gunicorn_error_ch.log'
loglevel = 'debug'
capture_output = True
