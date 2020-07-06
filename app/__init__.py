from flask import Flask
from config import Config # import the configuration settings creates
from flask_sqlalchemy import SQLAlchemy # represent the DB by a DB instance
from flask_migrate import Migrate # for the DB migration
from flask_login import LoginManager # For login sessions/also allows remember me

app = Flask(__name__)  # instance of a flask application
app.config.from_object(Config)
db = SQLAlchemy(app) # db instance
migrate = Migrate(app, db) # db migration, in case there are some structural changes to the DB, no need to rewrite the app
login = LoginManager(app)
login.login_view = 'login'# function name which will allow you to do a cool require login trick
# where once user has logged in they get redirected to the protected page


from app import routes, models  # routes defined for the URL and models for the DB model/schema