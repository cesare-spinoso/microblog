from app import app
# To export export FLASK_APP=microblog.py
# Then just run flask, flask run

# To make shell cmds less tedious (don't always need to write the import)
from app import db
from app.models import User, Post


@app.shell_context_processor
# For complete documentation of the query version with SQL alchemy go to SQLAlchemy doc page
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post}
