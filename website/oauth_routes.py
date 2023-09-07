from flask import Blueprint,url_for,redirect,flash,abort,request
from flask_login import login_user,current_user

from . import db
from .oauth import OAuthSignIn
from .models import User,Role


oauth_route = Blueprint("oauth_route",__name__)

#oauth login
@oauth_route.route("/login/<provider_name>", methods = ["POST"])
def oauth_login(provider_name):

    #check if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    
    #get URL for google login
    provider = OAuthSignIn.get_provider(provider_name)

    return provider.authorize(request)


#get information from provider
@oauth_route.route("/login/<provider_name>/callback/")
def callback(provider_name):

    # check if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    
    #get provider
    provider = OAuthSignIn.get_provider(provider_name)

    #get data
    email = provider.callback(request)
    
    if email:

        user = User.get_from_email(email)
        #wenn user bereits existiert und dritt party service nutzt einloggen
        if user:

            if user.is_third_party:
                login_user(user)
                flash("Sie haben sich erfolgreich eingeloggt", category="success")
                return redirect(url_for("views.home"))
            
            # user exists but is not 3rd party
            flash("Diese Email ist bereits unter einem normalen Account angemeldet", category="error")
            return redirect(url_for("views.home"))

        else:
            role = Role.get_role_by_name("Customer")

            new_user = User(
                email = email,
                # firstName = first_name,
                # lastName = last_name,
                thirdParty = True,
                role = role #Customer Role
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash("Sie haben sich erfolgreich registriert", category="success")
            return redirect(url_for("views.home"))

    else:
        flash(f"User email not available or not verified by {provider}", category="error")
        abort(400)