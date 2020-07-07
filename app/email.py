# Module that includes a helper function for sending an email
from flask_mail import Message
from app import app, mail
from flask import render_template
from threading import Thread

# Email sending can significantly slow down the web app
# Use multi-threading!!! So email is sent aysnchronously

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, text_html):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = text_html
    Thread(target=send_async_email, args=(app, msg)).start()
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token() # default expiry of 10 min
    send_email(subject='MICROBLOG: Reset password request',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               text_html=render_template('email/reset_password.html', user=user, token=token))