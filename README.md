# Flask Microblog
This is a microblog application designed with the help of the lovely [tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.

### Requirements

This code requires Python 3.* as well as the Flask library.

### Python Virtual Environment

Create a Python virtual environment called `venv` and install Flask dependencies

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Running the App

Run the application locally with `flask run` setting `FLASK_APP = microblog.py` and making sure the SQLite migrations are dealt with.


### Deployment
    
This flask app is deployed on Heroku and can be found [here](https://ces-microblog.herokuapp.com/login?next=%2F).
