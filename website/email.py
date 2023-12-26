from flask_mail import Message
from flask import current_app as app
from flask import render_template,url_for,Flask,copy_current_request_context
from website import mail
from .models import User,Order
from .data_validation import check_str_input_correct
from werkzeug.datastructures import FileStorage 
import os
from .ImageManager import OrderImageManager
from threading import Thread

def send_async_email(msg:Message):

    @copy_current_request_context
    def send_message(msg):
        mail.send(msg)


    sender = Thread(target=send_message,args=[msg,])
    sender.start()


def create_msg(to:str,subject:str,template:str,**kwargs) -> Message:
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
        msg.body = render_template("/email/" + template + ".html", **kwargs)
        msg.html = render_template("/email/" + template + ".html", **kwargs)
        return msg


# def send_password_reset_email(user:User) -> None:
#     '''
#         Sends a Email to a user, with Token, to reset the password of the user
#         :param: `user` is the user, who gets the email and whose password shall be reset
#     '''
#     if User.check_user_exists(user):
#         token = user.generate_password_reset_token()
#         send_email(user.email,"Password Reset","reset_password",user = user,token = token)

def create_order_img_msg_attachment(msg:Message,imgs:list[FileStorage]) -> Message:
    '''
        Creates the img message attachment of the order from the user
        :param: `msg` is the message to which it gets attached
        :param: `order_id` is the id of the order
        :param: `img_count` is the number of imgs the user sent in his request
    '''

    #for image attachment
    for index,img in enumerate(imgs):
        
        file_name = img.filename
        #get image as bytes
        content = img.stream.read()
        
        content_id = f"<Myimage-{index}>"
        
        msg.attach(file_name,'image/gif',content, 'inline', headers=[['Content-ID',content_id],])

    return msg


def send_customer_order_email(user:User,imgs:list[FileStorage],imgs_send = False) -> None:
    '''
        Sends an email,from a customer order, to the production sector, to build the guitar.
        :param: `user` is the User, who bought something
        :param: `imgs` are the images from the customer
        :param: `imgs_send` is if imgs are given
    '''

    if User.check_user_exists(user):

        #get cart of user
        order = Order.get_last_by_user(user)

        img_count = len(imgs)

        msg = create_msg("schneider_berghausen@web.de","Neue Bestellung","order", user = user, order = order,img_count = img_count)

        #for image attachment
        if imgs_send:
            msg_attached = create_order_img_msg_attachment(msg,imgs)

            send_async_email(msg_attached)

        else:
            send_async_email(msg)


def send_customer_confirmation_email(user:User,imgs:list[FileStorage],imgs_send = False) -> None:
    '''
        Sends an email to the customer to confirm his request
        :param: `user` is the Customer
        :param: `imgs` are the images from the customer
        :param: `imgs_send` is if imgs are given
    '''

    if User.check_user_exists(user):
        
        order = Order.get_last_by_user(user)
        img_count = len(imgs)

        msg = create_msg(user.email,"Eingangsbestätigung","customer_confirmation",order = order,user = user,img_count = img_count)

        if imgs_send:
            msg_attached = create_order_img_msg_attachment(msg,imgs)

            #attach logo
            msg_attached.attach("Logo.png","image/gif",open("./website/static/Bilder/Laptop/Logo.png","rb").read(),'inline', headers=[['Content-ID',"Logo"],])
            send_async_email(msg_attached)
        
        else:
            msg.attach("Logo.png","image/gif",open("./website/static/Bilder/Laptop/Logo.png","rb").read(),'inline', headers=[['Content-ID',"Logo"],])
            send_async_email(msg)


# def send_kontact_confirmation_email(user:User) ->  None:
#     '''
#         Sends an email to the customer to confirm his request
#     '''
#     if User.check_user_exists(user):
#         send_email(user.email,"Eingangsbestätigung","customer_confirmation")


