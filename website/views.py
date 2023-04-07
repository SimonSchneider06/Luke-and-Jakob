from flask import Blueprint,render_template,request,session,redirect,url_for
from flask_login import current_user,login_required
from .models import Guitar

from .helper_functions import add_cart_item

views = Blueprint('views',__name__)

@views.route('/',methods = ['GET','POST'])
def home():
    return render_template('home.html')

@views.route('/logged_in',methods = ['POST','GET'])
@login_required
def logged_in():
    return render_template("logged_in.html")

@views.route("/design-your-dream",methods = ["GET","POST"])
def design_your_dream():
    return render_template("design_your_dream.html")

# strg + k + c to comment multiple things at once (strg + k + u = uncomment)

@views.route("/cart",methods = ["POST", "GET"])
def shopping_cart():
    return render_template("shopping_cart.html")

@views.route("/shop")
def shop():
    products = Guitar.query.order_by(Guitar.id)
    return render_template("shop.html",products = products)  

@views.route("/product/<product_name>", methods = ["GET", "POST"]) #String default converter -> werkzeug routing rules
def product_site(product_name):
    #Gets product or returns 404 if it doesn't exist
    product = Guitar.query.filter_by(name = product_name).first_or_404()

    if request.method == "POST":

        #checks if session exists and isnt empty
        #if cart already exists adds product id of product to it
        if "cart" in session and session["cart"] != None:
            session["cart"] = add_cart_item(session["cart"],product.id)

        #else set it equal
        else:
            #makes session cart a list of product_lists, each product_list containing the product id and the number in the shopping_cart
            session["cart"] = [[product.id,1]]

        return redirect(url_for("views.product_site", product_name = product.name))

    return render_template("product.html", product = product)



@views.route("/cart-delete-product/<int:product_id>",methods = ["GET"])
def delete_cart_item(product_id):

    #checks if session cart exists
    if "cart" in session and session["cart"] != None:
        
        new_cart = []

        for product_list in session["cart"]:
            #if product_id not equal to deleted one, add it otherwise dont -> deleted
            if product_list[0] != product_id:
                new_cart.append(product_list)

        #set session equal to new list
        session["cart"] = new_cart

        #redirects user to shopping cart
        return redirect(url_for("views.shopping_cart"))
    
    else:
        #redirects user to shopping cart
        return redirect(url_for("views.shopping_cart"))
    

# route for changing the quantity of the items in the shopping cart
@views.route("/set_product_quantity/<int:product_id>/<int:quantity>", methods = ["GET"])
def cart_quantity(product_id,quantity):

    #checks if session cart exists
    if "cart" in session and session["cart"] != None:

        new_cart = []

        for product_list in session["cart"]:
            #if product_id equal to selected one, change quantity
            if product_list[0] == product_id:
                product_list[1] = quantity

            new_cart.append(product_list)

        #set session equal to new list
        session["cart"] = new_cart

        #redirects user to shopping cart
        return redirect(url_for("views.shopping_cart"))
    
    else:
        #redirects user to shopping cart
        return redirect(url_for("views.shopping_cart"))