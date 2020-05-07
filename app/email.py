from flask_mail import Message
from . import mail
from flask import current_app,render_template
from threading import Thread

#程序处理request的过程都是在requestcontext之中，但是另开了一个线程来处理邮件发送，它本身没有app context
#所以需要传入app，并获取context
#搞个多线程，多线程就需要

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
    sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    # mail.send(msg)
    return thr