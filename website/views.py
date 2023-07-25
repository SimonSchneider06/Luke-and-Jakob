from flask import Blueprint,render_template,request,session,redirect,url_for,flash
from flask_login import login_required,current_user
from .models import Guitar
import stripe

from .helper_functions import add_cart_item
from .email import send_customer_order_email

views = Blueprint('views',__name__)

@views.route('/',methods = ['GET','POST'])
def home():
    return render_template('home.html')

@views.route("/about_us",methods = ["GET"])
def about_us():
    return render_template("about_us.html")

@views.route('/logged_in',methods = ['POST','GET'])
@login_required
def logged_in():
    return render_template("logged_in.html")

@views.route("/design-your-dream",methods = ["GET","POST"])
def design_your_dream():
    return render_template("design_your_dream.html")

# strg + k + c to comment multiple things at once (strg + k + u = uncomment)

#shopping cart site
@views.route("/cart",methods = ["GET"])
def shopping_cart():
    return render_template("shopping_cart.html")

#zur kasse btn pressed 
@views.route("/checkout", methods = ["POST"])
def checkout():
    #checks if shopping cart exists
    if session["cart"]:

        line_items_new = []

        #loop through the product lists
        for product_list in session["cart"]:

            #get guitar by id
            product = Guitar.query.filter_by(id = product_list[0]).first()

            #get stripe price id and quantity
            price_id = product.stripe_price_id
            quantity = product_list[1]

            #format it, for stripe checkout session
            item = {
                "price": price_id,
                "quantity":quantity,
            }

            line_items_new.append(item)


        #create stripe checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items = line_items_new,
                mode = "payment",
                success_url = url_for("views.home", _external = True),
                cancel_url = url_for("views.shopping_cart", _external = True)
            )

        except Exception as e:
            str(e)

        return redirect(checkout_session.url,code = 303)

@views.route("/webhook",methods = ["POST"])
def stripe_webhook():
    pass

@views.route("/shop")
def shop():
    products = Guitar.query.order_by(Guitar.id)
    return render_template("shop.html",products = products)  

@views.route("/product/<product_name>", methods = ["GET", "POST"]) #String default converter -> werkzeug routing rules
def product_site(product_name):
    #Gets product or returns 404 if it doesn't exist
    product = Guitar.query.filter_by(name = product_name).first_or_404()
    return render_template("product.html", product = product)
