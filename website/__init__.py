from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
from flask_mail import Mail
#import stripe

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app(config_name):
    #creating app 
    app = Flask(__name__)
    
    #getting config data from config file
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #initializing the database, mail module , and migration module to easily update the db
    db.init_app(app) 
    migrate = Migrate(app,db)
    mail.init_app(app)

    #if should redirect all http to https requests
    if app.config["SSL_REDIRECT"]:
        
        from flask_sslify import SSLify
        sslify = SSLify(app)

    #configuring the stripe account
    # stripe.api_key = app.config["PAYMENT_SERVICES"]["stripe"]["secret_key"]

    #importing the blueprints
    from .views import views
    from .actions import actions
    # from .auth import auth
    # from .admin import admin
    # from .shopping import shopping
    # from .stripeRoutes import stripeBlueprint
    # from .oauth_routes import oauth_route

    #adding the blueprints to the app
    app.register_blueprint(views,url_prefix = "/")
    app.register_blueprint(actions,url_prefix = "/")
    # app.register_blueprint(auth,url_prefix = "/")
    # app.register_blueprint(admin,url_prefix = "/")
    # app.register_blueprint(shopping,url_prefix = "/")
    # app.register_blueprint(stripeBlueprint,url_prefix = "/")
    # app.register_blueprint(oauth_route, url_prefix = "/")

    #adding the errorpages to the app
    from .errorhandling import errors
    errors(app)

    #database management
    from .models import User

    with app.app_context():
        db.create_all()

    #making logging in 
    # login_manager.login_view = "auth.login"
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     # old, depreceated
    #     # return User.query.get(int(id))
    #     return db.session.get(User,id)
    
    # #import methods to be used in jinja 
    # from .jinja_functions import get_product_by_id
    # from .ImageManager import ImageManager
    # from .shoppingCart import CartManager
    from .ImageManager import OrderImageManager
    from .cookies import cookies_asked, cookies_allowed

    # #integrates function to jinja2 
    app.jinja_env.globals.update(OrderImageManager = OrderImageManager)
    app.jinja_env.globals.update(cookies_asked = cookies_asked)
    app.jinja_env.globals.update(cookies_allowed = cookies_allowed)
    # app.jinja_env.globals.update(ImageManager = ImageManager)
    # app.jinja_env.globals.update(CartManager = CartManager)
    # app.jinja_env.globals.update(get_product_by_id = get_product_by_id)
    # app.jinja_env.globals.update(GoogleAPIKey = app.config["OAUTH_CREDENTIALS"]["google"]["id"])

    return app
