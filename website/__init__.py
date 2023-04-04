from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from os import walk
from flask_login import LoginManager,current_user
from flask_migrate import Migrate
from flask import current_app as app

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7lK83(?ki2.Pieqr_!Mn]iZ'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 15
    app.config["UPLOAD_EXTENSIONS"] = [".JPG", ".png"]
    app.config["UPLOAD_PATH"] = "./website/static/Bilder/Produktbilder"

    db.init_app(app) 
    migrate = Migrate(app,db)

    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views,url_prefix = "/")
    app.register_blueprint(auth,url_prefix = "/")
    app.register_blueprint(admin,url_prefix = "/")

    from .errorhandling import errors
    errors(app)

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from .helper_functions import get_file_by_product_name,get_product_by_id,get_total_price

    #integrates function to jinja2 
    app.jinja_env.globals.update(get_file_by_product_name = get_file_by_product_name)
    app.jinja_env.globals.update(get_product_by_id = get_product_by_id)
    app.jinja_env.globals.update(get_total_price = get_total_price)

    return app
