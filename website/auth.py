from flask import Blueprint,render_template,request,flash,redirect,url_for,abort
from .models import User,Role
from . import db
from flask_login import login_user,logout_user,current_user,login_required
from .email import send_password_reset_email
from .oauth import OAuthSignIn

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
                passwort = passwort1,
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

        user = User.query.filter_by(email = email).first()

        if user and user.thirdParty != True: # user should exist and not be a registered through 3rd party, like google
            if user.verifyPassword(passwort):
                flash("Erfogreich Angemeldet",category = "success")
                login_user(user,remember = user.rememberMe)
                return redirect(url_for("views.home"))

            else:
                flash("Passwort ist Falsch",category="error")

        else:
            flash("Email existiert nicht", category = "error")

    return render_template("auth/login.html")

#oauth login
@auth.route("/login/<provider_name>", methods = ["POST"])
def oauth_login(provider_name):
    
    #get URL for google login
    provider = OAuthSignIn(provider_name)
    #get request_uri to ask for data
    request_uri = provider.get_request_uri(request)

    return redirect(request_uri)

#get information from provider
@auth.route("/login/<provider_name>/callback/")
def callback(provider_name):
    # get authorization code
    auth_code = request.args.get("code")
    
    #get provider
    provider = OAuthSignIn(provider_name)
    
    #get userinfo
    userinfo_response = provider.token_request(request,auth_code)

    #check email verification
    if userinfo_response.json().get("email_verified"):
        print(userinfo_response)
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        first_name = userinfo_response.json()["given_name"]
        last_name = userinfo_response.json()["family_name"]

        user = User.query.filter_by(email = users_email).first()
        #wenn user bereits existiert einloggen
        if user:
            login_user(user)
            flash("Sie haben sich erfolgreich eingeloggt", category="success")
            return redirect(url_for("views.home"))

        else:
            new_user = User(
                email = users_email,
                firstName = first_name,
                lastName = last_name,
                thirdParty = True,
                role_id = 2 #Customer Role
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Sie haben sich erfolgreich registriert", category="success")
            return redirect(url_for("views.home"))

    else:
        flash(f"User email not available or not verified by {provider}", category="error")
        abort(400)



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
        
            return redirect(url_for("views.home"))
        
        except:
            flash("Es ist ein Fehler unterlaufen bitte versuchen sie es nochmal")
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
        
        user = User.query.filter_by(email = email).first()

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