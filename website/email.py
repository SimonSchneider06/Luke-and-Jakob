from flask_mail import Message
from flask import current_app as app
from flask import render_template
from website import mail

#send email

def send_email(to,subject,template,**kwargs):
    msg = Message(app.config["MAIL_PREFIX"] + " " + subject, sender = app.config["MAIL_USERNAME"], recipients = [to])
    msg.body = render_template("/email/" + template + ".txt", **kwargs)
    msg.html = render_template("/email/" + template + ".html", **kwargs)
    mail.send(msg)

#send password reset email
def send_password_reset_email(user):
    token = user.generate_password_reset_token()
    send_email(user.email,"Password Reset","reset_password",user = user,token = token)