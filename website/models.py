from __future__ import annotations  #needed in User.verify_password_reset_token, so that return value is able to be User
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import jwt
from time import time
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
from sqlalchemy import select
from .debug import check_str_input_correct

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

    order = db.Column(db.PickleType)    # for the shopping-cart/order of the customer

    #relationships
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))



    def set_order(self,cart:list) -> None:
        '''
            Takes the cart and sets the order column in the database
            :param: `cart` is a list of dictionaries
        '''
        #store it as pickle object
        self.order = pickle.dumps(cart)


    def get_order(self) -> list:
        '''
            Returns the order as list of dictionaries
        '''
        #restore the pickle object to its original list
        return pickle.loads(self.order)


    def generate_password_reset_token(self,expiration = 600) -> str:
        '''
            generates a token to reset the passwort
            Returns a string
            :param: `expiration` is the time after which the token expires, in seconds
        '''
        if expiration <= 0:
            raise ValueError("Token Expiration Time can't be <= 0")

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
        # stmt =  select(User).where(User.id == id)
        # return db.session.scalar(stmt)
        return db.session.get(User,id)


    @staticmethod
    def check_user_exists(user:User) -> bool:
        '''
            Checks whether the User exists in the Database or not
            Returns true or false
            :param: `user` is of type User
        '''

        if type(user) != User:
            raise TypeError("user should be of Type User")

        if user.id == None:
            return False

        # search_query = select(User).where(User.id == user.id)
        # result = db.session.scalar(search_query)

        result = db.session.get(User,user.id)

        if result:
            return True
        else:
            return False


    @property
    def password(self):
        raise AttributeError("Password is not a readable Attribute")

    @password.setter
    def password(self,password:str):
        self.passwort_hash = generate_password_hash(password,method = "scrypt")

    def verifyPassword(self,password:str) -> bool:
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


    @staticmethod
    def check_guitar_exists(guitar:Guitar) -> bool:
        '''
            Checks whether the guitar exists in the database or not
            Returns a true or false
            :param: `guitar` is of type Guitar
        '''

        if type(guitar) != Guitar:
            raise TypeError("guitar should be of Type Guitar")

        if guitar.id == None:
            return False

        # search_query = select(Guitar).where(Guitar.id == guitar.id)
        # result = db.session.scalar(search_query)

        result = db.session.get(Guitar,guitar.id)

        if result:
            return True
        else:
            return False
        

    @staticmethod
    def check_guitar_exists_by_name(guitar_name:str) -> bool:
        '''
            Checks whether the guitar exists in the database or not
            Returns a true or false
            :param: `guitar_name` is the name of the guitar
        '''

        if check_str_input_correct(guitar_name,"guitar_name","check_guitar_exists_by_name"):

            search_query = select(Guitar).where(Guitar.name == guitar_name)
            result = db.session.scalar(search_query)

            if result:
                return True
            else:
                return False