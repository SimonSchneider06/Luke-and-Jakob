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
        name = request.form.get("name")
        telNumber = request.form.get("telNumber")
        alter = request.form.get("alter")
        passwort1 = request.form.get("passwort1")
        passwort2 = request.form.get("passwort2")
        role = Role.query.filter_by(name = "Customer").first()

        user = User.query.filter_by(email = email).first()

        if user:
            flash("Email existiert bereits ",category="error")
        if len(email) < 4:
            flash("Email muss länger als 4 Zeichen sein",category = "error")
        elif len(name) < 4:
            flash("Vor- und Nachname müssen länger als 4 Zeichen sein",category = "error")
        elif len(telNumber) != 12:
            flash("Ihre Telefon Nummer muss 12 Zeichen lang sein",category = "error")
        elif passwort1 != passwort2:
            flash("Die Passwörter stimmen nicht überein",category = "error")
        elif len(passwort1) < 7:
            flash("Das Passwort muss mindestens 7 Zeichen lang sein",category = "error")
        else:
            new_user = User(email = email,
                name = name,
                telNumber = telNumber,
                alter = alter,
                passwort = generate_password_hash(passwort1,method = "sha256"),
                role = role)
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember = True)
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
                login_user(user,remember = True)
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
        name = request.form.get("name")
        telNumber = request.form.get("telNumber")
        alter = request.form.get("alter")

        user = current_user

        if len(name) < 4:
            flash("Vor- und Nachname müssen länger als 4 Zeichen sein",category = "error")
        elif len(telNumber) != 14:
            flash("Ihre Telefon Nummer muss 14 Zeichen lang sein",category = "error")
        else:
            try:
                user.name = name
                user.telNumber = telNumber
                user.alter = alter
                
                db.session.commit()
                flash("Erfolgreich Daten geändert",category = "success")
            
                return redirect(url_for("views.logged_in"))
            
            except:
                flash("Es ist ein Fehler unterlaufen bitte versuchen sie es nochmal")
                return render_template("change_account_data.html")

    return render_template("auth/change_account_data.html")

#Passwort vergessen--------------------------------

@auth.route("/forgot_password")
def password_reset():
    return render_template("/auth/forgot_password.html")