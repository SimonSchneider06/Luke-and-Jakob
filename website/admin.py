from flask import Blueprint, render_template,url_for,request,flash, redirect

from .models import User, Guitar, Role
from . import db
from .decorators import admin_required
import os
from .ImageManager import ImageManager
from .data_validation import check_list_of_str_correct

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

        # check if guitar with this name already exists
        elif Guitar.check_guitar_exists_by_name(name):
            flash("Gitarren Name existiert schon", category="error")
            return redirect(url_for("admin.add_product"))
        
        #checks if all fields contain information
        elif check_list_of_str_correct([name,price,stock,description,stripe_price_id]) == False:
            flash("Bitte füllen sie alle Felder aus", category = "error")
            return redirect(url_for("admin.add_product"))
        
        #check if price and stock are digits
        elif price.isdigit() == False or stock.isdigit() == False:
            flash("Geben Sie bei Preis und Anzahl nur Zahlen ein", category = "error")
            return redirect(url_for("admin.add_product"))
 
        else:
        
            for image in front_img:

                #check each image
                if not imageManager.verify_image(image):
                    flash("Bilder waren nicht gültig oder nicht vorhanden, bitte versuchen Sie es erneut", category="error")
                    return redirect(url_for('admin.add_product'))
            
            #flash("Image saved successfully", category = "success")

            #after looping through the images store the guitar model

            new_guitar = Guitar(name = name,
            price = price,
            stock = stock,
            description = description,
            stripe_price_id = stripe_price_id)
            
            db.session.add(new_guitar)
            db.session.commit()

            # save image after product got created and stored in db and not in above
            # loop because 
            # 1) there might be a wrong image in front image, so got redirected, but
            #       it's not the first one, so the others are already saved, but product
            #       not created
            # 2) imageManager.save_image_by... needs to get path from another imageManager
            #       method which throws error, if product doesn't exist

            for index, image in enumerate(front_img):
                
                imageManager.save_image_by_product_name_and_number(image,index,name)

            flash("Erfolgreich neues Modell hinzugefügt")
            return redirect(url_for("admin.admin_page"))

    return render_template("admin/add_product.html")


#------------------------change product------------------------------------


@admin.route("admin/change_product/<int:id>", methods = ["POST","GET"])
def change_product(id):
    # get guitar
    product = Guitar.query.filter_by(id = id).first_or_404()

    if request.method == "POST":
        product_name = request.form.get("product-name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        description = request.form.get("description")
        stripe_price_id = request.form.get("stripe_price_id")

        input_data = [product_name,price,stock,description,stripe_price_id]

        #check if new images recieved
        img_0 = request.files.get("img-0")
        img_1 = request.files.get("img-1")
        img_2 = request.files.get("img-2")
        img_3 = request.files.get("img-3")
        img_4 = request.files.get("img-4")

        #search for guitars with same name
        #if guitar has name but is same id as changeable product 
        #so products are identical 
        #if id not equal -> different guitar with this name exists so dont allow 
        # overwriting of name
        guitar_with_name = Guitar.get_by_name(product_name)

        # first check if even exists
        if guitar_with_name:
            if guitar_with_name.id != product.id:
                flash("Gitarre mit diesem Namen existiert schon", category = "error")
                return redirect(url_for("admin.change_product", id = product.id))
        
        # verify data
        if check_list_of_str_correct(input_data) == False:
            flash("Eingegebene Daten sind nicht richtig", category = "error")
            return redirect(url_for("admin.change_product",id = product.id))
        
        #check if price and stock are digits
        elif price.isdigit() == False or stock.isdigit() == False:
            flash("Geben Sie bei Preis und Anzahl nur Zahlen ein", category = "error")
            return redirect(url_for("admin.change_product",id = product.id))
        

        # verify images
        if imageManager.verify_image(img_0) == False or imageManager.verify_image(img_1) == False or \
        imageManager.verify_image(img_2) == False or imageManager.verify_image(img_3) == False or \
        imageManager.verify_image(img_4) == False:
            flash("Bilder nicht gültig, versuchen sie es mit anderen",category="error")
            return redirect(url_for("admin.change_product",id = product.id)) 

        else:
                        
            imageManager.save_image_by_product_name_and_number(img_0,0,product.name)
            imageManager.save_image_by_product_name_and_number(img_1,1,product.name)
            imageManager.save_image_by_product_name_and_number(img_2,2,product.name)
            imageManager.save_image_by_product_name_and_number(img_3,3,product.name)
            imageManager.save_image_by_product_name_and_number(img_4,4,product.name)


            product.name = product_name
            product.price = price
            product.stock = stock
            product.description = description
            product.stripe_price_id = stripe_price_id
            db.session.commit()
            flash("Product Daten erfolgreich verändert",category = "success")
            return redirect(url_for("admin.admin_page"))
           
    return render_template("admin/change_product.html",product = product,os = os)

#---------------------delete product-------------------------------------

@admin.route("admin/delete_product/<int:id>",methods = ["GET"])
def delete_product(id):
    product_to_delete = Guitar.query.filter_by(id = id).first_or_404()
    try:
        imageManager.delete_directory_by_product_name(product_to_delete.name)

        db.session.delete(product_to_delete)
        db.session.commit()
        flash("Produkt erfolgreich gelöscht", category = "success")
        return redirect(url_for("admin.admin_page"))

    except: # pragma: no cover (in case something unexpected happend), not testable
        flash("Es ist ein Fehler unterlaufen bitte versuchen sie es erneut", category = "error")
        return redirect(url_for("admin.admin_page"))
    
    
#-----------------------change user role-----------------------------

@admin.route("/admin/change_user/<int:id>",methods = ["POST","GET"])
def change_user(id):
    user = User.query.filter_by(id = id).first_or_404()
    
    if request.method == "POST":
        role_name = request.form.get("selectRole")

        if role_name == "": #if nothing selected throw error
            flash("Bitte waehlen Sie eine Rolle aus", category = "error")
            return redirect(url_for("admin.change_user",id = user.id))
        
        
        user_role = Role.query.filter_by(name = role_name).first()

        if user_role:
            
            try:
                user.role_id = user_role.id
                db.session.commit()
                flash("User Rolle erfolgreich geändert", category = "success")
                return redirect(url_for("admin.admin_page"))

            except: #pragma: no cover   in case something unexpected happens
                 flash("Es ist leider ein Fehler unterlaufen. Bitte versuchen sie es erneut", category = "error")
                 return redirect(url_for("admin.change_user",id = user.id))
            
        # wenn die rolle nicht existiert
        else:
            flash("Diese Rolle existiert nicht", category = "error")
            return redirect(url_for("admin.change_user",id = user.id))

    return render_template("admin/change_user.html",user = user)


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