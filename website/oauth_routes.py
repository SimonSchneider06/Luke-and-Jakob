from flask import Blueprint,url_for,redirect,request,flash,abort
from flask_login import login_user

from . import db
from .oauth import OAuthSignIn
from .models import User


oauth_route = Blueprint("oauth_route",__name__)

#oauth login
@oauth_route.route("/login/<provider_name>", methods = ["POST"])
def oauth_login(provider_name):
    
    #get URL for google login
    provider = OAuthSignIn(provider_name)
    #get request_uri to ask for data
    request_uri = provider.get_request_uri(request)

    return redirect(request_uri)


#get information from provider
@oauth_route.route("/login/<provider_name>/callback/")
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