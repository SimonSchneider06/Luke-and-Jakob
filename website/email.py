from flask_mail import Message
from flask import current_app as app
from flask import render_template
from website import mail
from .models import User
import datetime
from .data_validation import check_str_input_correct
import os


def send_email(to:str,subject:str,template:str,**kwargs) -> None:
    '''
        Sends an Email from the Company's Account to somebody else
        :param: `to` is the Email from the recipient; the Email address, from the person who gets the email
        :param: `subject` is the Topic, What the Email is about
        :param: `template` is the Email template, which gets used, for example: password_reset,...
        :param: `**kwargs` are values which may be needed in some email_templates
    '''

    #checking if input type correct
    if check_str_input_correct(to,"to","send_email") and \
        check_str_input_correct(subject,"subject","send_email") and \
        check_str_input_correct(template,"template","send_email"):

        #check if template path exists
        if not os.path.exists(f"./website/templates/email/{template}.txt"):
            raise ValueError("Email Template in send_email doesn't exist")

        msg = Message(app.config["MAIL_PREFIX"] + " " + subject, sender = app.config["MAIL_USERNAME"], recipients = [to])
        msg.body = render_template("/email/" + template + ".txt", **kwargs)
        msg.html = render_template("/email/" + template + ".html", **kwargs)
        mail.send(msg)


def send_password_reset_email(user:User) -> None:
    '''
        Sends a Email to a user, with Token, to reset the password of the user
        :param: `user` is the user, who gets the email and whose password shall be reset
    '''
    if User.check_user_exists(user):
        token = user.generate_password_reset_token()
        send_email(user.email,"Password Reset","reset_password",user = user,token = token)


def send_customer_order_email(user:User) -> None:
    '''
        Sends an email,from a customer order, to the production sector, to build the guitar.
        :param: `user` is the User, who bought something
    '''

    if User.check_user_exists(user):
        # get time of buying
        buying_date = datetime.datetime.utcnow()

        #get cart of user
        order = user.get_order()

        send_email("schneider_berghausen@web.de","Neue Bestellung","order",user = user, order = order,buying_date = buying_date)