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

def create_order_img_msg_attachment(msg:Message,order_id:int,img_count:int) -> Message:
    '''
        Creates the img message attachment of the order from the user
        :param: `msg` is the message to which it gets attached
        :param: `order_id` is the id of the order
        :param: `img_count` is the number of imgs the user sent in his request
    '''

    #for image attachment
    for i in range(img_count):
        img_path = OrderImageManager().get_image_path_by_order_and_img_number(order_id,i)

        file_ext = OrderImageManager().get_file_path_ext(img_path)
        
        file_name = f'{i}{file_ext}'
        
        content_id = f"<Myimage-{i}>"
        
        msg.attach(file_name,'image/gif',open(f"./website/static/Bilder/Kundenauftragsbilder/{order_id}/{file_name}", 'rb').read(), 'inline', headers=[['Content-ID',content_id],])

    return msg


def send_customer_order_email(user:User,img_count:int) -> None:
    '''
        Sends an email,from a customer order, to the production sector, to build the guitar.
        :param: `user` is the User, who bought something
        :param: `img_count` is the number of images in the order
    '''

    if User.check_user_exists(user):

        #get cart of user
        order = Order.get_last_by_user(user)

        msg = create_msg("kontakt@lukeandjakob.com","Neue Bestellung","order", user = user, order = order,img_count = img_count)

        #for image attachment
        msg_attached = create_order_img_msg_attachment(msg,order.id,img_count)

        send_async_email(msg_attached)


def send_customer_confirmation_email(user:User,img_count:int) -> None:
    '''
        Sends an email to the customer to confirm his request
        :param: `user` is the Customer
        :param: `img_count` is the number of images in the user request
    '''
    if User.check_user_exists(user):
        
        order = Order.get_last_by_user(user)

        msg = create_msg(user.email,"Eingangsbestätigung","customer_confirmation",order = order,user = user,img_count = img_count)

        msg_attached = create_order_img_msg_attachment(msg,order.id,img_count)

        #attach logo
        msg_attached.attach("Logo.png","image/gif",open("./website/static/Bilder/Laptop/Logo.png","rb").read(),'inline', headers=[['Content-ID',"Logo"],])

        #mail.send(msg_attached)
        # thr = Thread(target = send_async_email,args = [app,msg_attached])
        # thr.start()
        # return thr
        send_async_email(msg_attached)


# def send_kontact_confirmation_email(user:User) ->  None:
#     '''
#         Sends an email to the customer to confirm his request
#     '''
#     if User.check_user_exists(user):
#         send_email(user.email,"Eingangsbestätigung","customer_confirmation")


