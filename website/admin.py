from flask import Blueprint, render_template,url_for,request,flash, redirect, abort
from flask_login import login_required, current_user
from .models import User, Guitar, Role
from . import db
from .decorators import admin_required
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
import shutil

#import imghdr to validate image file and size
import imghdr

admin = Blueprint("admin",__name__)

#--------------admin page mit überblick--------------------------------

@admin.route("/admin",methods = ["POST", "GET"])
@login_required
@admin_required()
def admin_page():
    our_users = User.query.order_by(User.id)
    products = Guitar.query.order_by(Guitar.id)
    return render_template("admin.html",our_users = our_users,products = products)


#-----------add product-----------------------------------------------------

@admin.route("/admin/add_product",methods=["POST","GET"])
@login_required
@admin_required()
def add_product():
    if request.method == "POST":
        name = request.form.get("product-name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        
        front_img = request.files.getlist("image-deck")
        uploaded_images = request.files.getlist("image")

        # adds the other images after the front_img so 
        # they are all in one list with the front img first

        front_img.extend(uploaded_images)

        
        guitar_name = Guitar.query.filter_by(name = name).first()
        if guitar_name:
            flash("Gitarren Name existiert schon", category="error")

        else:
            folder_path = save_uploaded_img(front_img,name)
            if folder_path == None:
                flash("Images were not valid please try again", category="error")
            else:
                #flash("Image saved successfully", category = "success")

            #after looping through the images store the guitar model

                new_guitar = Guitar(name = name,
                price = price,
                stock = stock)
                
                db.session.add(new_guitar)
                db.session.commit()
                flash("Erfolgreich neues Modell hinzugefügt")
                return redirect(url_for("admin.admin_page"))

    return render_template("add_product.html")


#------------------------change product------------------------------------


@admin.route("admin/change_product/<int:id>", methods = ["POST","GET"])
@login_required
@admin_required()
def change_product(id):
    product = Guitar.query.filter_by(id = id).first()
    if request.method == "POST":
        product_name = request.form.get("product-name")
        price = request.form.get("price")
        stock = request.form.get("stock")

        front_img = request.files.getlist("image-deck")
        uploaded_images = request.files.getlist("image")

        # adds the other images after the front_img so 
        # they are all in one list with the front img first

        front_img.extend(uploaded_images)


        #search for guitars with same name
        guitar_with_name = Guitar.query.filter_by(name = product_name).first()


        #if guitar has name but is same id as changeable product 
        #so products are identical 
        #if id not equal -> different guitar with this name exists so dont allow overwriting of name

        if guitar_with_name.id != product.id:
            flash("Gitarre mit diesem Namen existiert schon", category = "error")

        else:
            if product:
                
                #checks the images
                folder_path = save_uploaded_img(front_img,product_name, True)
                if folder_path == None:
                    flash("Images were not valid please try again", category="error")

                else:

                    try:

                        product.name = product_name
                        product.price = price
                        product.stock = stock
                        db.session.commit()
                        flash("Product Daten erfolgreich verändert",category = "success")
                        return redirect(url_for("admin.admin_page"))
                        
                    except:
                        flash("Es ist ein Fehler unterlaufen bitte versuchen sie es erneut", category = "error")
                        return render_template("change_product.html",product = product)
        

    return render_template("change_product.html",product = product)

#---------------------delete product-------------------------------------

@admin.route("admin/delete_product/<int:id>",methods = ["POST","GET"])
@login_required
@admin_required()
def delete_product(id):
    product_to_delete = Guitar.query.filter_by(id = id).first_or_404()
    try:
        del_dir_from_guitar_name(product_to_delete.name)

        db.session.delete(product_to_delete)
        db.session.commit()
        flash("Product deleted successfully", category = "success")
        return redirect(url_for("admin.admin_page"))

    except:
        flash("Es ist ein Fehler unterlaufen bitte versuchen sie es erneut", category = "error")
        return redirect(url_for("admin.admin_page"))
    
    
#-----------------------change user role-----------------------------

@admin.route("/admin/change_user/<int:id>",methods = ["POST","GET"])
@login_required
@admin_required()
def change_user(id):
    user = User.query.filter_by(id = id).first()
    role = Role.query.filter_by(id = user.role_id).first()
    if request.method == "POST":
        role_name = request.form.get("role")
        user_role = Role.query.filter_by(name = role_name).first()

        if user_role:
            try:
                user.role_id = user_role.id
                db.session.commit()
                flash("Account Role changed successfully", category = "success")
                return redirect(url_for("admin.admin_page"))

            except:
                flash("Es ist leider ein Fehler unterlaufen. Bitte versuchen sie es erneut", category = "error")
                return render_template("change_user.html",role = role,our_user = user)

    return render_template("change_user.html",role = role,our_user = user)

#----------------------------delete user----------------------------------------

@admin.route("admin/delete_user/<int:id>", methods = ["POST","GET"])
@login_required
@admin_required()
def delete_user(id):
    user_to_delete = User.query.filter_by(id = id).first()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully", category = "success")
        return redirect(url_for("admin.admin_page"))

    except:
        flash("Es ist ein Fehler aufgetreten", category = "error")
        return redirect(url_for("admin.admin_page"))

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