from __future__ import annotations  #needed in User.verify_password_reset_token, so that return value is able to be User
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import jwt
from time import time
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

#------------user and roles--------------------------

class User(db.Model,UserMixin):
    '''
        Manages the User, defines how the database table looks
        has methods for working with it easier
    '''

    # How the Database table is defined

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
    passwort_hash = db.Column(db.String(50))
    #remember user after login
    rememberMe = db.Column(db.Boolean)
    #date added
    date_added = db.Column(db.DateTime(timezone = True),default = func.now())
    #3rd party
    thirdParty = db.Column(db.Boolean)  #used to check if google or other login is needed

    #relationships
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))


    def generate_password_reset_token(self,expiration = 600) -> str:
        '''
            generates a token to reset the passwort
            Returns a string
            :param: `expiration` is the time after which the token expires, in seconds
        '''
        return jwt.encode(
            {"reset_password":self.id,"exp":time() + expiration},app.config["SECRET_KEY"],algorithm="HS256"
        )


    @staticmethod
    def verify_password_reset_token(token:str) -> (User | None):
                                                    # this User needs the import 'from __future__ import annotations', so that a type of object User can be
                                                    # returned in the class User.
        '''
            verify a password reset token, if token valid return user with given id ,else return none 
        '''
        try:
            id = jwt.decode(token,app.config["SECRET_KEY"],algorithms="HS256")["reset_password"]
        except:
            return
        return User.query.get(id)
    
    @property
    def password(self):
        raise AttributeError("Password is not a readable Attribute")
    
    @password.setter
    def password(self,password):
        self.passwort_hash = generate_password_hash(password,"sha256")

    def verifyPassword(self,password) -> bool:
        return check_password_hash(self.passwort_hash,password)


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
    stripe_price_id = db.Column(db.String(100))
    description = db.Column(db.Text)