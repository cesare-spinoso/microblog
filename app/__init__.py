from flask import Flask
from config import Config # import the configuration settings creates
from flask_sqlalchemy import SQLAlchemy # represent the DB by a DB instance
from flask_migrate import Migrate # for the DB migration
from flask_login import LoginManager # For login sessions/also allows remember me
import logging # For logging the stack trace, the email sending is covered with this package
from logging.handlers import SMTPHandler # for the email logging
from logging.handlers import RotatingFileHandler # for the file logging
import os

app = Flask(__name__)  # instance of a flask application
app.config.from_object(Config)
db = SQLAlchemy(app) # db instance
migrate = Migrate(app, db) # db migration, in case there are some structural changes to the DB, no need to rewrite the app
login = LoginManager(app)
login.login_view = 'login'# function name which will allow you to do a cool require login trick
# where once user has logged in they get redirected to the protected page


if not app.debug: # Only send when not debugging
    if app.config['MAIL_SERVER']: # And a mail server is configured
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


from app import routes, models, errors  # routes defined for the URL and models for the DB model/schema