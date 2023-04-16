from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User,Role
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,logout_user,current_user,login_required

auth = Blueprint("auth",__name__)

#sign up and login and logout ---------------------------------------------------------------------------------

@auth.route("/signUp",methods=['GET',"POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        #name
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        #address
        street = request.form.get("street")
        houseNumber = request.form.get("houseNumber")
        plz = request.form.get("PLZ")
        city = request.form.get("city")
        country = request.form.get("selectCountry")
        #password
        passwort1 = request.form.get("passwort1")
        passwort2 = request.form.get("passwort2")
        rememberMe = request.form.get("rememberMe") #can be on or off
        role = Role.query.filter_by(name = "Customer").first()

        user = User.query.filter_by(email = email).first()

        #convert rememberMe in boolean value
        if rememberMe == "on":
            rememberMe = True
        else:
            rememberMe = False

        if user:
            flash("Email existiert bereits ",category="error")
        if len(email) < 4:
            flash("Email muss länger als 4 Zeichen sein",category = "error")
        elif passwort1 != passwort2:
            flash("Die Passwörter stimmen nicht überein",category = "error")
        elif len(passwort1) < 7:
            flash("Das Passwort muss mindestens 7 Zeichen lang sein",category = "error")
        else:
            new_user = User(email = email,
                firstName = firstName,
                lastName = lastName,
                street = street,
                houseNumber = houseNumber,
                plz = plz,
                city = city,
                country = country,
                rememberMe = rememberMe,
                passwort = generate_password_hash(passwort1,method = "sha256"),
                role = role)
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember = new_user.rememberMe)
            flash("Erfolgreich Registriert",category = "success")
            
            return redirect(url_for("views.logged_in"))

    return render_template("auth/sign_up.html")

@auth.route('/login',methods = ['GET',"POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        passwort = request.form.get("passwort")

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.passwort,passwort):
                flash("Erfogreich Angemeldet",category = "success")
                login_user(user,remember = user.rememberMe)
                return redirect(url_for("views.logged_in"))

            else:
                flash("Passwort ist Falsch",category="error")

        else:
            flash("Email existiert nicht")

    return render_template("auth/login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

#-------change user data-----------------------------

@auth.route("/change_user" , methods = ["GET", "POST"])
@login_required
def change_user_data():
    if request.method == "POST":

        #name
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        #address
        street = request.form.get("street")
        houseNumber = request.form.get("houseNumber")
        plz = request.form.get("PLZ")
        city = request.form.get("city")
        country = request.form.get("selectCountry")
        #remember user
        rememberMe = request.form.get("rememberMe") #can be on or off
        
        #convert rememberMe to boolean value
        if rememberMe == "on":
            rememberMe = True
        else:
            rememberMe = False

        user = current_user

        try:
            user.firstName = firstName
            user.lastName = lastName
            user.street = street
            user.houseNumber = houseNumber
            user.plz = plz
            user.city = city
            user.country = country
            user.rememberMe = rememberMe
            
            db.session.commit()
            flash("Erfolgreich Daten geändert",category = "success")
        
            return redirect(url_for("views.logged_in"))
        
        except:
            flash("Es ist ein Fehler unterlaufen bitte versuchen sie es nochmal")
            return redirect(url_for("auth.change_user_data"))

    return render_template("auth/change_account_data.html")

#Passwort vergessen--------------------------------

@auth.route("/forgot_password")
def password_reset():
    return render_template("/auth/forgot_password.html")


#account page

@auth.route("/account")
@login_required
def account_page():
    return render_template("/auth/account.html")