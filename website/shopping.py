from flask import Blueprint,session,flash,redirect,url_for
from .cartManager import CartManager
from .models import Guitar 

cartManager = CartManager()

shopping = Blueprint("shopping",__name__) 


@shopping.route("/add_to_cart/<int:product_id>",methods = ["POST"])
def add_to_cart(product_id:int):
    #get product or return 404 error
    product = Guitar.query.filter_by(id = product_id).first_or_404()

    # check if session cart exists
    if "cart" in session and session["cart"] != None:
        session["cart"] = cartManager.add_product(product.id,session["cart"])
    else:
        session["cart"] = [{"id": product.id,"quantity":1}]

    flash("Produkt erfolgreich im Einkaufswagen hinzugefügt", category = "success")
    return redirect(url_for('views.product_site',product_name = product.name))



@shopping.route("/delete_from_cart/<int:product_id>",methods = ["GET"])
def delete_from_cart(product_id:int):
    product = Guitar.query.filter_by(id = product_id).first_or_404()

    if "cart" in session and session["cart"] != None:
        session["cart"] = cartManager.delete_product(product_id,session["cart"])
        flash("Produkt erfolgreich aus dem Einkaufswagen gelöscht", category = "success")

    return redirect(url_for("views.shopping_cart"))


@shopping.route("/set_product_quantity/<int:product_id>/<int:quantity>",methods = ["GET"])
def set_product_quantity(product_id:int,quantity:int):
    product = Guitar.query.filter_by(id = product_id).first_or_404()

    if "cart" in session and session["cart"] != None:
        session["cart"] = cartManager.set_quantity(product_id,session["cart"],quantity)
        flash("Produktmenge erfolgreich geändert",category = "success")

    return redirect(url_for("views.shopping_cart"))