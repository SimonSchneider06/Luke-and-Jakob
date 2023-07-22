from flask_mail import Message
from flask import current_app as app
from flask import render_template,session
from website import mail
from .models import User
import datetime

def send_email(to:str,subject:str,template:str,**kwargs) -> None:
    '''
        Sends an Email from the Company's Account to somebody else
        :param: `to` is the Email from the recipient; the Email address, from the person who gets the email
        :param: `subject` is the Topic, What the Email is about
        :param: `template` is the Email template, which gets used, for example: password_reset,...
        :param: `**kwargs` are values which may be needed in some email_templates
    '''
    msg = Message(app.config["MAIL_PREFIX"] + " " + subject, sender = app.config["MAIL_USERNAME"], recipients = [to])
    msg.body = render_template("/email/" + template + ".txt", **kwargs)
    msg.html = render_template("/email/" + template + ".html", **kwargs)
    mail.send(msg)


def send_password_reset_email(user:User) -> None:
    '''
        Sends a Email to a user, with Token, to reset the password of the user
        :param: `user` is the user, who gets the email and whose password shall be reset
    '''
    token = user.generate_password_reset_token()
    send_email(user.email,"Password Reset","reset_password",user = user,token = token)

#send email with order to us, to fullfill the order
def send_customer_order_email(user:User) -> None:
    '''
        Sends an email,from a customer order, to the production sector, to build the guitar.
        :param: `user` is the User, who bought something
    '''
    #get the order from session_cookies
    order = session["cart"]

    # get time of buying
    buying_date = datetime.datetime.utcnow()

    send_email("schneider_berghausen@web.de","Neue Bestellung","order",user = user, order = order,buying_date = buying_date)