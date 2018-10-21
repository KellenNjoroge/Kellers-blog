from flask_mail import Message
# from manage import app
from .models import Email
from . import mail
from flask import render_template
import os


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_subscriptions(new_subscription):
    send_email('Subscribed to Kellers Blog', sender=os.environ.get('MAIL_USERNAME'),
               recepients=[new_subscription.email_data],
               text_body=render_template('emails/subscribed.txt', new_subscription=new_subscription),
               html_body=render_template('emails/subscribed.html', new_subscription=new_subscription))


def send_blogs(blog):
    subscribers = Email.query.order_by('-id').all()
    for subscriber in subscribers:
        send_email('**New Post Alert!!', sender=os.environ.get('MAIL_USERNAME'), recepients=[subscriber.email_data],
                   text_body=render_template('emails/new_blog.txt', blog=blog, subscriber=subscriber),
                   html_body=render_template('emails/new_blog.html', blog=blog, subscriber=subscriber))
