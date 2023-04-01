from flask import Blueprint,render_template,request,session,redirect,url_for
from flask_login import current_user,login_required
from .models import Guitar

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

    #checks if session exists and isnt empty
    if "cart" in session and session["cart"] != None:
        products = []

        for product_id in session["cart"]:
            product = Guitar.query.filter_by(id = product_id).first()
            
            #append product to list
            products.append(product)

    else:
        products = None

    return render_template("shopping_cart.html",products = products)

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
            #makes empty list of shopping cart
            cart = []

            #goes through current session and adds every product in list
            for product_id in session["cart"]:
                cart.append(product_id)
                
            #checks if product already in shopping cart and if not adds it in cart
            if product.id not in cart:
                cart.append(product.id)

            #save cart in session
            session["cart"] = cart


        #else set it equal
        else:
            session["cart"] = [product.id]

        return redirect(url_for("views.product_site", product_name = product.name))

    return render_template("product.html", product = product)



@views.route("/cart-delete-product/<int:product_id>",methods = ["GET"])
def delete_cart_item(product_id):
    
    #checks if product in session
    if product_id in session["cart"]:

        #makes an list to work with
        cart = session["cart"]

        #loops through elements of cart
        for id in cart:
            #if id in cart equals product_id , delete item
            if id == product_id:
                cart.remove(id)

        #set session equal to new list
        session["cart"] = cart

        #redirects user to shopping cart
        return redirect(url_for("views.shopping_cart"))
    
    else:
        #redirects user to shopping cart
        return redirect(url_for("views.shopping_cart"))