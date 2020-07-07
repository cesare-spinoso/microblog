import os
basedir = os.path.abspath(os.path.dirname(__file__)) # main directory of the app


# Use a class to keep all the configuration settings
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # To protect against CSRF

    # For the database management
    # Set the DB location
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # the DB location is either in predefined os env or in hardcoded app.db directory
    SQLALCHEMY_TRACK_MODIFICATION = False # So not notified everytime there is a modif to the DB

    # Receiving stack trace emails
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['cesare.spinoso@gmail.com']

    # For the pagination
    POSTS_PER_PAGE = 10

