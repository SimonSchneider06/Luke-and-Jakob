from os import walk
from flask import current_app as app
from .models import Guitar
from flask import session, render_template, abort
from flask_mail import Message
from website import mail
import os
#import imghdr to validate image file and size
import imghdr
import shutil
from werkzeug.utils import secure_filename


# adds products to shopping cart
def add_cart_item(cart, add_product_id):

    #new cart
    new_cart = []
    #variable, which checks if the product already is in the shopping_cart
    is_new_id = True

    #loops through the cart to get each list
    for product_list in cart:
        #first item = product_id, second = menge
        #if new item is already in cart, add 1 to menge
        if product_list[0] == add_product_id:
            product_list[1] += 1
            is_new_id = False
        #append list
        new_cart.append(product_list)

    #if id isnt in cart, because if statement from above never executed, add it
    if is_new_id:
        new_cart.append([add_product_id,1])

    return new_cart


#------gets file path -------------------------------------

def get_file_by_product_name(product_name,img_number):

    folder = app.config["UPLOAD_PATH"] + f"/{product_name}"
    
    path = f"Bilder/Produktbilder/{product_name}"
    
    for (_, __ , filenames) in walk(folder):
        for file in filenames:
            file_name = file.split(".")[0]

            #filename is a string !!!!!!
            if file_name == f"{img_number}":
                full_path = path + f"/{file}"
                return full_path
    
    return None

#gets product by product_id
def get_product_by_id(id):
    product = Guitar.query.filter_by(id = id).first()
    return product

#get gesamtpreis
def get_total_price():
    
    total_price = 0

    if session["cart"]:
        
        #loop through the product_lists
        for product_list in session["cart"]:
            
            #get product
            product = Guitar.query.filter_by(id = product_list[0]).first()

            #price of product * menge of product = price
            price = product.price * product_list[1]

            total_price += price

    return total_price


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

#check and save img
def check_save_img(image,guitar_name,number):
    if image != None:
    
    #checks if filename not empty, so if file got recieved
        if secure_filename(image.filename) != "":
            #save image
            save_image_with_number(image,guitar_name,number)


#save images by their specific number to not overwrite existing ones
def save_image_with_number(image, guitar_name,number):

    #number = image.split("_")[1]    # image = img_0 ; so get the 0
    file_ext = os.path.splitext(image.filename)[1]

    # if not valid abort  -- "\" makes the if go over the next line
    if file_ext not in app.config["UPLOAD_EXTENSIONS"] or file_ext != validate_image(image.stream):
        abort(400)

    file_path = app.config["UPLOAD_PATH"] + f"/{guitar_name}/{number}.{file_ext}"

    image.save(file_path)

# ------------------------------validate image function----------------------

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None,header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "JPG")

#saves , and checks images from array---------------------------------------------------------

def save_uploaded_img(img_list,guitar_name):
    #create count number
    i = 0

    #loops through the uploaded_images array
    for uploaded_img in img_list:
        #makes the filename secure

        filename = secure_filename(uploaded_img.filename)
        #filename = uploaded_img.filename

        #if filename is empty -> no file received so if not empty -> file received
        if filename != "":
            
            #splits the extension of the filename to look if its valid or not 
            file_ext = os.path.splitext(filename)[1]
            # print(file_ext)

            # if not valid abort  -- "\" makes the if go over the next line
            if file_ext not in app.config["UPLOAD_EXTENSIONS"] or file_ext != validate_image(uploaded_img.stream):
                abort(400)

            new_folder_path = app.config["UPLOAD_PATH"] + f"/{guitar_name}"
            if not os.path.exists(new_folder_path):
                os.mkdir(new_folder_path)

            #save img in ./website/static/Bilder/Productbilder/name of the guitar so there cant be duplicates
            path = os.path.join(new_folder_path,str(i) + file_ext )
            uploaded_img.save(path)
            #adding one to image count
            i += 1 

    return new_folder_path if i >= 1 else None


#----------delete directory of image by guitar---------

def del_dir_from_guitar_name(guitar_name):
    #gets path
    img_path = app.config["UPLOAD_PATH"] + f"/{guitar_name}"
    #Deletes directory with imgs
    shutil.rmtree(img_path)