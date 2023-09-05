from flask import Blueprint, render_template,url_for,request,flash, redirect
from flask_login import login_required
from .models import User, Guitar, Role
from . import db
from .decorators import admin_required
import os
from .ImageManager import ImageManager

admin = Blueprint("admin",__name__)

imageManager = ImageManager()

@admin.before_request
@admin_required()   # if now not logged in get 403 error
def before_request():
    pass

#--------------admin page mit überblick--------------------------------

@admin.route("/admin",methods = ["POST", "GET"])
def admin_page():
    our_users = User.query.order_by(User.id)
    products = Guitar.query.order_by(Guitar.id)
    return render_template("admin/admin.html",our_users = our_users,products = products)


#-----------add product-----------------------------------------------------

@admin.route("/admin/add_product",methods=["POST","GET"])
def add_product():
    if request.method == "POST":
        name = request.form.get("product-name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        description = request.form.get("description")
        stripe_price_id = request.form.get("stripe_price_id")
        
        front_img = request.files.getlist("image-deck")
        uploaded_images = request.files.getlist("image")

        # adds the other images after the front_img so 
        # they are all in one list with the front img first

        front_img.extend(uploaded_images)

        # check front_img list is not empty
        if front_img == []:
            flash("Bitte setzen sie Bilder ein", category = "error")
            return redirect(url_for("admin.add_product"))
        
        
        guitar_name = Guitar.query.filter_by(name = name).first()
        #checks if guitarname already exists
        if guitar_name:
            flash("Gitarren Name existiert schon", category="error")
            return redirect(url_for("admin.add_product"))
        
        #checks if all fields contain information
        elif name == "" or price == "" or stock == "" or description == "" or stripe_price_id == "":
            flash("Bitte füllen sie alle Felder aus", category = "error")
            return redirect(url_for("admin.add_product"))

        else:
        
            for index,image in enumerate(front_img):

                #check each image
                if not imageManager.verify_image(image):
                    flash("Bilder waren nicht gültig oder nicht vorhanden, bitte versuchen Sie es erneut", category="error")
                    return redirect(url_for('admin.add_product'))
                
                #save if not not redirected
                imageManager.save_image_by_product_name_and_number(image,index,guitar_name)
            
            #flash("Image saved successfully", category = "success")

            #after looping through the images store the guitar model

            new_guitar = Guitar(name = name,
            price = price,
            stock = stock,
            description = description,
            stripe_price_id = stripe_price_id)
            
            db.session.add(new_guitar)
            db.session.commit()
            flash("Erfolgreich neues Modell hinzugefügt")
            return redirect(url_for("admin.admin_page"))

    return render_template("admin/add_product.html")


#------------------------change product------------------------------------


@admin.route("admin/change_product/<int:id>", methods = ["POST","GET"])
def change_product(id):
    product = Guitar.query.filter_by(id = id).first()
    if request.method == "POST":
        product_name = request.form.get("product-name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        description = request.form.get("description")
        stripe_price_id = request.form.get("stripe_price_id")

        #check if new images recieved
        img_0 = request.files.get("img-0")
        img_1 = request.files.get("img-1")
        img_2 = request.files.get("img-2")
        img_3 = request.files.get("img-3")
        img_4 = request.files.get("img-4")

        # front_img = request.files.getlist("image-deck")
        # uploaded_images = request.files.getlist("image")

        # adds the other images after the front_img so 
        # they are all in one list with the front img first

        # front_img.extend(uploaded_images)


        #search for guitars with same name
        guitar_with_name = Guitar.query.filter_by(name = product_name).first()


        #if guitar has name but is same id as changeable product 
        #so products are identical 
        #if id not equal -> different guitar with this name exists so dont allow overwriting of name

        if guitar_with_name.id != product.id:
            flash("Gitarre mit diesem Namen existiert schon", category = "error")

        else:
            if product:
                        
                imageManager.save_image_by_product_name_and_number(img_0,0,product.name)
                imageManager.save_image_by_product_name_and_number(img_1,1,product.name)
                imageManager.save_image_by_product_name_and_number(img_2,2,product.name)
                imageManager.save_image_by_product_name_and_number(img_3,3,product.name)
                imageManager.save_image_by_product_name_and_number(img_4,4,product.name)


                #checks the images
                # folder_path = save_uploaded_img(front_img,product_name)
                # if folder_path == None:
                #     flash("Images were not valid please try again", category="error")

                

                try:

                    product.name = product_name
                    product.price = price
                    product.stock = stock
                    product.description = description
                    product.stripe_price_id = stripe_price_id
                    db.session.commit()
                    flash("Product Daten erfolgreich verändert",category = "success")
                    return redirect(url_for("admin.admin_page"))
                    
                except:
                    flash("Es ist ein Fehler unterlaufen bitte versuchen sie es erneut", category = "error")
                    # return render_template("change_product.html",product = product)
                    return redirect(url_for("admin.change_product",id = product.id ))
        

    return render_template("admin/change_product.html",product = product,os = os)

#---------------------delete product-------------------------------------

@admin.route("admin/delete_product/<int:id>",methods = ["POST","GET"])
def delete_product(id):
    product_to_delete = Guitar.query.filter_by(id = id).first_or_404()
    try:
        imageManager.delete_directory_by_product_name(product_to_delete.name)

        db.session.delete(product_to_delete)
        db.session.commit()
        flash("Product deleted successfully", category = "success")
        return redirect(url_for("admin.admin_page"))

    except:
        flash("Es ist ein Fehler unterlaufen bitte versuchen sie es erneut", category = "error")
        return redirect(url_for("admin.admin_page"))
    
    
#-----------------------change user role-----------------------------

@admin.route("/admin/change_user/<int:id>",methods = ["POST","GET"])
def change_user(id):
    user = User.query.filter_by(id = id).first()
    
    if request.method == "POST":
        role_name = request.form.get("selectRole")

        if role_name == "": #if nothing selected throw error
            flash("Bitte wählen sie eine Rolle aus", category = "error")
            return redirect(url_for("admin.change_user",id = user.id))
        
        
        user_role = Role.query.filter_by(name = role_name).first()

        if user_role:
            try:
                user.role_id = user_role.id
                db.session.commit()
                flash("Account Role changed successfully", category = "success")
                return redirect(url_for("admin.admin_page"))

            except:
                flash("Es ist leider ein Fehler unterlaufen. Bitte versuchen sie es erneut", category = "error")
                return redirect(url_for("admin.change_user",id = user.id))

    return render_template("admin/change_user.html",user = user)

#----------------------------delete user----------------------------------------

@admin.route("admin/delete_user/<int:id>", methods = ["POST","GET"])
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


#----------delete single img from product
@admin.route("/delete_product_img/<product_name>/<int:number>", methods = ["GET"])
def delete_product_img(product_name, number):

    product = Guitar.query.filter_by(name = product_name).first_or_404()
    file_path = imageManager.get_image_path_by_product_name_and_number(product_name,number)
    #flash(file_path)
    full_path = f"./website/static/{file_path}"

    if os.path.exists(full_path):
        os.remove(full_path)
        flash(f"Bild {number} erfolgreich gelöscht", category = "success")
    else:
        flash("Bild existiert nicht", category = "error")
        return redirect(url_for("admin.change_product", id = product.id))    

    return redirect(url_for("admin.change_product", id = product.id))