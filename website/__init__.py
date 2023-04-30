from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from os import walk
from flask_login import LoginManager,current_user
from flask_migrate import Migrate
from flask import current_app as app
from config import config
from flask_mail import Mail
import stripe

db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()

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

    #configuring the stripe account
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]

    #importing the blueprints
    from .views import views
    from .auth import auth
    from .admin import admin

    #adding the blueprints to the app
    app.register_blueprint(views,url_prefix = "/")
    app.register_blueprint(auth,url_prefix = "/")
    app.register_blueprint(admin,url_prefix = "/")

    #adding the errorpages to the app
    from .errorhandling import errors
    errors(app)

    #database management
    from .models import User

    with app.app_context():
        db.create_all()

    #making logging in 
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    #import methods to be used in jinja 
    from .helper_functions import get_file_by_product_name,get_product_by_id,get_total_price

    #integrates function to jinja2 
    app.jinja_env.globals.update(get_file_by_product_name = get_file_by_product_name)
    app.jinja_env.globals.update(get_product_by_id = get_product_by_id)
    app.jinja_env.globals.update(get_total_price = get_total_price)

    return app
