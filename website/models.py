from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import jwt
from time import time
from flask import current_app as app

#------------user and roles--------------------------

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True)
    #name
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    #address
    street = db.Column(db.String(50))
    houseNumber = db.Column(db.String(10))
    plz = db.Column(db.String(10))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    #password
    passwort = db.Column(db.String(50))
    #remember user after login
    rememberMe = db.Column(db.Boolean)
    #date added
    date_added = db.Column(db.DateTime(timezone = True),default = func.now())

    #relationships
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))


    #generate token to reset password using jwt
    def generate_password_reset_token(self,expiration = 600):
        return jwt.encode(
            {"reset_password":self.id,"exp":time() + expiration},app.config["SECRET_KEY"],algorithm="HS256"
        )

    #to verify a password reset token, if token valid return user with given id ,else return none
    @staticmethod
    def verify_password_reset_token(token):
        try:
            id = jwt.decode(token,app.config["SECRET_KEY"],algorithms="HS256")["reset_password"]
        except:
            return
        return User.query.get(id)


class Role(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(150),unique = True)
    users = db.relationship("User", backref = "role")


#class Guitar(db.Model):
    #id = db.Column(db.Integer, primary_key = True)

#what information to store:
    #Product----- Name , Price, 3d Model, Image, 
    #- Color, Size, Shape, Wood, 

class Guitar(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(150), unique = True)
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    description = db.Column(db.Text)