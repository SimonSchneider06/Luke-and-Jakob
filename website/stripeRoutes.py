from flask import Blueprint,redirect,url_for,session,request 
from .shoppingCart import StripeCartConverter 
import stripe
from flask import current_app as app
from .email import send_customer_order_email
from flask_login import current_user,login_required
import json
from .models import User
from . import db

stripeCartConverter = StripeCartConverter()

stripeBlueprint = Blueprint("stripeBlueprint",__name__) 

@login_required
@stripeBlueprint.route("/checkout-stripe",methods = ["POST"])
def stripe_checkout():

    #get list formated for stripe

    if "cart" in session and session["cart"] != None:
        stripe_list = stripeCartConverter.convert_all_dicts(session["cart"])

        user = current_user
        user.set_order(session["cart"])
        db.session.add(user)
        db.session.commit()

        #create stripe checkout session
        try: 
            checkout_session = stripe.checkout.Session.create(
                    client_reference_id = current_user.id, 
                    line_items = stripe_list,
                    mode = "payment",
                    success_url = url_for("views.home", _external = True),
                    cancel_url = url_for("views.shopping_cart", _external = True)
                )
        
        except Exception as e:  #pragma: no cover
            str(e)      # pragma: no cover

        return redirect(checkout_session.url,code = 303)
    


@stripeBlueprint.route("/webhook", methods = ["POST"])
def stripe_webhook():
    
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload,sig_header,app.config["PAYMENT_SERVICES"]["stripe"]["endpoint_key"]
        )
        
    except Exception as e:
        return "Invalid Response", 400 

    if event["type"] == "checkout.session.completed":

        #client_reference_id = payload["data"]["object"]["client_reference_id"]
        # payload is a string -> needs to be converted to json to get user id
        # client_reference_id
        payload_json = json.loads(payload)
        client_reference_id = payload_json["data"]["object"]["client_reference_id"]

        #get User
        user = User.query.filter_by(id = client_reference_id).first()
        send_customer_order_email(user)
        

    return "Success",200