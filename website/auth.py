from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User,Role
from . import db
from flask_login import login_user,logout_user,current_user,login_required
from .email import send_password_reset_email
from .value_checker import check_list_of_str_correct

auth = Blueprint("auth",__name__)

#sign up and login and logout ---------------------------------------------------------------------------------

@auth.route("/signUp",methods=['GET',"POST"])
def sign_up():
    if request.method == "POST":

        # get data from html

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

        #checking the user_data
        user_check = User.check_all_user_data_correct(email = email,
                                            firstName= firstName,
                                            lastName= lastName,
                                            houseNumber= houseNumber,
                                            street = street,
                                            plz = plz,
                                            city = city,
                                            country = country,
                                            password1 = passwort1,
                                            password2 = passwort2,
                                            rememberMe = rememberMe)
        
        if user_check == True:
            # if successful create new user

            # convert rememberMe
            rememberMe_converted = User.convert_rememberMe(rememberMe)

            new_user = User(email = email,
                firstName = firstName,
                lastName = lastName,
                street = street,
                houseNumber = houseNumber,
                plz = plz,
                city = city,
                country = country,
                rememberMe = rememberMe_converted,
                password = passwort1,
                thirdParty = False,
                role = role)
            
            # add to db
            db.session.add(new_user)
            db.session.commit()

            #login
            login_user(new_user,remember = new_user.rememberMe)

            #flash message
            flash("Erfolgreich Registriert",category = "success")
            
            #redirect to homepage
            return redirect(url_for("views.home"))
        
        else:
            flash(user_check, category="error")
            return redirect(url_for('auth.sign_up'))

    return render_template("auth/sign_up.html")


#login page; POST method gets normal login
@auth.route('/login',methods = ['GET',"POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        passwort = request.form.get("password")

        if User.check_email_exists(email) == True:

            if User.check_is_third_party(email) == False:
                # user should exist an not be registered through 3rd party

                user = User.get_from_email(email)
        
                if user.verifyPassword(passwort):
                    
                    flash("Erfolgreich Angemeldet",category = "success")
                    login_user(user,remember = user.rememberMe)
                    
                    return redirect(url_for("views.home"))

                else:
                    flash("Passwort ist Falsch",category="error")
                    return redirect(url_for("auth.login"))
                
            else:
                flash("Sie haben sich ueber einen Drittanbieter registriert", category = "error")
                return redirect(url_for("auth.login"))

        else:
            flash("Email existiert nicht", category = "error")
            return redirect(url_for('auth.login'))

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

        user:User = current_user

        if check_list_of_str_correct([firstName,lastName,street,houseNumber,plz,city,country,rememberMe]):

            user.set_full_name(firstName,lastName)
            user.set_address(street,houseNumber,plz,city,country)
            user.set_rememberMe(rememberMe)

            flash("Erfolgreich Daten geaendert",category = "success")
        
            return redirect(url_for("views.home"))

        else:
    
            flash("Es ist ein Fehler unterlaufen bitte versuchen sie es nochmal", category = "error")
            return redirect(url_for("auth.change_user_data"))

    return render_template("auth/change_account_data.html")


#Passwort vergessen--------------------------------

@auth.route("/forgot_password",methods = ["POST","GET"])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        #gets email from submit field
        email = request.form.get("email")
        
        user = User.get_from_email(email)

        #checks if user exists
        if user:
            send_password_reset_email(user)

        flash("Ihnen wurde eine Email gesendet", category = "success")
        return redirect(url_for("auth.login"))


    return render_template("/auth/forgot_password.html")


#site for new password after password reset through email
@auth.route("/reset_password/<token>",methods = ["GET","POST"])
def new_password(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('views.home'))
    
    user = User.verify_password_reset_token(token)
    #if token not verified
    if not user:
        return redirect(url_for("views.home"))
    
    if request.method == "POST":
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2:
            user.password = password1
            db.session.commit()
            flash("Ihr Passwort wurde erfolgreich zurückgesetzt",category = "success")
            return redirect(url_for('views.home'))
        
    return render_template("auth/new_password.html")


#account page
@auth.route("/account")
@login_required
def account_page():
    return render_template("/auth/account.html")