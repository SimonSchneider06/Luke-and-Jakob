from flask import Blueprint,render_template
from . import db
# from .models import Guitar


views = Blueprint('views',__name__)

@views.route('/',methods = ['GET'])
def Home():
    return render_template('home.html', active = "Home")

@views.route("/about_us",methods = ["GET"])
def About():
    return render_template("about_us.html", active = "About")

# expired
# @views.route('/logged_in',methods = ['POST','GET'])
# @login_required
# def logged_in():
#     return render_template("logged_in.html")

@views.route("/services", methods = ["GET"])
def Services():
    return render_template("services.html", active = "Services")

@views.route("/nachhaltigkeit", methods = ["GET"])
def Nachhaltigkeit():
    return render_template("nachhaltigkeit.html", active = "Nachhaltigkeit")

@views.route("/kontakt", methods = ["GET"])
def Kontakt():
    return render_template("contact.html", active = "Kontakt")

# @views.route("/design-your-dream",methods = ["GET","POST"])
# def design_your_dream():
#     return render_template("design_your_dream.html")

# strg + k + c to comment multiple things at once (strg + k + u = uncomment)


#--------------------------------------------------for shop site------
#shopping cart site
# @views.route("/cart",methods = ["GET"])
# def shopping_cart():
#     return render_template("shopping_cart.html")


# @views.route("/shop")
# def shop():
#     products = db.session.query(Guitar).order_by(Guitar.id)
#     return render_template("shop.html",products = products)  

# @views.route("/product/<product_name>", methods = ["GET", "POST"]) #String default converter -> werkzeug routing rules
# def product_site(product_name):
#     #Gets product or returns 404 if it doesn't exist
#     product = Guitar.query.filter_by(name = product_name).first_or_404()
#     return render_template("product.html", product = product)
