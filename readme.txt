Continue from Chapter 6 User Page:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

Note:
username: admin
password: root

username: Taco
password: caT

username: jonn
pwd: doe

To debug:
export FLASK_DEBUG=1

And then rerun

In debug mode the application restarts when you make changes.

To test the mail server:
run  python -m smtpd -n -c DebuggingServer localhost:8025
and in another terminal
export MAIL_SERVER=localhost
MAIL_PORT=8025

or use
export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=cesare.spinoso
export MAIL_PASSWORD=****

Make sure you have enabled less secure on Google