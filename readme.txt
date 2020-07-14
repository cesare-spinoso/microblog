Continue from Chapter 6 User Page:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

Note:
username: admin
password: root

username: Taco
password: caT

username: jonn
pwd: doe

user: billybob
pwd: doe
email: c.sdp

To debug:
export FLASK_DEBUG=1

And then rerun

In debug mode the application restarts when you make changes.

To test the mail server:
run  python -m smtpd -n -c DebuggingServer localhost:8025
and in another terminal
export MAIL_SERVER=localhost
export MAIL_PORT=8025

or use
export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=cesare.spinoso
export MAIL_PASSWORD=****

Make sure you have enabled less secure on Google

For emailing (for password reset):
As far as the actual sending of emails, Flask has a popular extension called Flask-Mail that can make the task very easy. As always, this extension is installed with pip:

(venv) $ pip install flask-mail

The password reset links will have a secure token in them. To generate these tokens, I'm going to use JSON Web Tokens, which also have a popular Python package:

(venv) $ pip install pyjwt

****In case your email testing isnt working try first running the consol one with
run  python -m smtpd -n -c DebuggingServer localhost:8025
and in another terminal
export MAIL_SERVER=localhost
export MAIL_PORT=8025

AND THEN set up the shell version by first (outside of shell) doing all the exports for using Gmail
THEN run flask shell and use the following:
from flask_mail import Message
from app import mail
msg = Message('Hello', sender=app.config['ADMINS'][0], recipients=['cesare.spinoso@gmail.com'])
msg.body = 'text body'
msg.html = '<h1>Thank you for choosing microblog. Bye!</h1>'
mail.send(msg)

For the bootstrap:
pip install flask-bootstrap

For the time zone moment.js and flask package:
pip install flask-moment

The moment class requires a timestamp in ISO format to be passed:
{{ year }}-{{ month }}-{{ day }}T{{ hour }}:{{ minute }}:{{ second }}{{ timezone }}