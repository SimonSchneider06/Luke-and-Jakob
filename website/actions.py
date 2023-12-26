from flask import Blueprint,redirect,url_for,request,flash
from .ImageManager import OrderImageManager
from .data_validation import check_list_of_str_correct
from .models import Order, User
from . import db
from .email import send_customer_order_email,send_customer_confirmation_email

actions = Blueprint('actions',__name__)

order_image_manager = OrderImageManager()

@actions.route("/submit-contact-request/", methods = ["POST"])
def contact_form():
    #get information from contact form
    service = request.form.get("servicesSelect")
    email = request.form.get("email")
    name = request.form.get("name")
    description = request.form.get("description")
    imgs = request.files.getlist("images")
    print(imgs[0].filename)

    if imgs[0].filename != "":
        #check if information correct
        if check_list_of_str_correct([service,email,name,description]) and \
            order_image_manager.verify_image_list(imgs):

            #get user, if exists, get from db, else create new one
            # geht davon aus, dass andere Personen andere Emails verwenden
            if User.check_email_exists(email):

                user = User.get_from_email(email)

            else:
                user = User(
                    email = email,
                    name = name,
                )

                db.session.add(user)
                db.session.commit()

            #to save the images order_id is needed, so save order first

            new_order = Order(
                service = service,
                description = description,
                confirmed = False,
                users = user.id
            )

            db.session.add(new_order)
            db.session.commit()

            order = Order.get_last_by_user(user)

            # save images
            order_image_manager.save_image_list_by_order_id(imgs,order.id)

            img_count = len(imgs)

            send_customer_order_email(user,img_count,True)
            send_customer_confirmation_email(user,img_count,True)

            flash("Ihre Anfrage wurde erfolgreich abgesendet", category = "success")
            return redirect(url_for("views.Home"))
        
        else:
            flash("Bitte füllen Sie alle angegebenen Felder aus.", category = "error")
            flash("Bei Bilddateien sind nur '.JPG' und '.png' erlaubt (max 5 MB)", category = "error")
            return redirect(url_for("views.Home"))
    
    else:
        if check_list_of_str_correct([service,email,name,description]):

            #get user, if exists, get from db, else create new one
            # geht davon aus, dass andere Personen andere Emails verwenden
            if User.check_email_exists(email):

                user = User.get_from_email(email)

            else:
                user = User(
                    email = email,
                    name = name,
                )

                db.session.add(user)
                db.session.commit()

            #to save the images order_id is needed, so save order first

            new_order = Order(
                service = service,
                description = description,
                confirmed = False,
                users = user.id
            )

            db.session.add(new_order)
            db.session.commit()

            img_count = len(imgs)

            send_customer_order_email(user,img_count)
            send_customer_confirmation_email(user,img_count)

            flash("Ihre Anfrage wurde erfolgreich abgesendet", category = "success")
            return redirect(url_for("views.Home"))
        
        else:
            flash("Bitte füllen Sie alle angegebenen Felder aus.", category = "error")
            return redirect(url_for("views.Home"))