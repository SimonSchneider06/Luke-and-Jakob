from flask import Blueprint,flash,redirect,url_for,session 
from .cartManager import StripeCartConverter 
import stripe

stripeCartConverter = StripeCartConverter()

stripeBlueprint = Blueprint("stripeBlueprint",__name__) 

@stripeBlueprint.route("/checkout-stripe",methods = ["POST"])
def stripe_checkout():

    #get list formated for stripe

    if "cart" in session and session["cart"] != None:
        stripe_list = stripeCartConverter.convert_all_dicts(session["cart"])

        #create stripe checkout session
        try: 
            checkout_session = stripe.checkout.Session.create(
                    line_items = stripe_list,
                    mode = "payment",
                    success_url = url_for("views.home", _external = True),
                    cancel_url = url_for("views.shopping_cart", _external = True)
                )
        
        except Exception as e:
            str(e)

        return redirect(checkout_session.url,code = 303)
    


@stripeBlueprint.route("/webhook", methods = ["POST"])
def stripe_webhook():
    pass