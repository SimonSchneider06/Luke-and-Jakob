from __future__ import annotations  #needed in User.verify_password_reset_token, so that return value is able to be User
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import jwt
from time import time
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
from sqlalchemy import select,desc
from .data_validation import check_str_input_correct, check_str_correct,convert_rememberMe

#------------user and order--------------------------
class Order(db.Model):
    '''
        Manages the User, defines how the database table looks
        has methods to make working with it easier
    '''

    # How the Database table is defined

    id = db.Column(db.Integer,primary_key = True)
    service = db.Column(db.String(20))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone = True),default = func.now())
    confirmed = db.Column(db.Boolean)
    users = db.Column(db.Integer,db.ForeignKey("user.id"))

    @staticmethod
    def get_last_by_user(user:User) -> Order | None:
        '''
            retrieve all Orders from the given User
            :param: `user` is the user 
        '''
        if user != None:
            query = select(Order).filter(Order.users == user.id).order_by(desc(Order.date))
            # # print(query)
            result = db.session.scalar(query)
            # # print(result)
            # result = db.session.execute(query).scalars()
            #result = db.session.query(Order).filter(Order.users == user.id).order_by(Order.date)
            return result
        return None
    

class User(db.Model,UserMixin):
    '''
        Manages the User, defines how the database table looks
        has methods to make working with it easier
    '''

    # How the Database table is defined

    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(50),unique = True)
    #name
    # firstName = db.Column(db.String(50))
    # lastName = db.Column(db.String(50))
    name = db.Column(db.String(50))
    orders = db.relationship("Order", backref = "user")
    #address
    # street = db.Column(db.String(50))
    # houseNumber = db.Column(db.String(10))
    # plz = db.Column(db.String(10))
    # city = db.Column(db.String(50))
    # country = db.Column(db.String(50))
    #password
    # passwort_hash = db.Column(db.String(50))
    #remember user after login
    # rememberMe = db.Column(db.Boolean)
    #date added
    # date_added = db.Column(db.DateTime(timezone = True),default = func.now())
    #3rd party
    # thirdParty = db.Column(db.Boolean)  #used to check if google or other login is needed

    # orders = db.Column(db.PickleType)    # for the shopping-cart/order of the customer

    #relationships
    # role_id = db.Column(db.Integer,db.ForeignKey("role.id"))


    # def set_order(self,cart:list) -> None:
    #     '''
    #         Takes the cart and sets the order column in the database
    #         :param: `cart` is a list of dictionaries
    #     '''
    #     #store it as pickle object
    #     if type(cart) != list:
    #         raise TypeError("cart should be of Type list")
        
    #     if cart == []:
    #         raise ValueError("cart shouldn't be an empty list")

    #     self.order = pickle.dumps(cart)


    # def get_order(self) -> list:
    #     '''
    #         Returns the order as list of dictionaries
    #     '''
    #     #restore the pickle object to its original list  
    #     if self.order == None:
    #         raise ValueError("self.order shouldn't be empty")  
    #     return pickle.loads(self.order)


    # def set_firstName(self,firstName:str) -> bool:
    #     '''
    #         Sets the firstName of the user.
    #         Returns True if successful else False
    #         :param: `firstName` is the firstName of the user
    #     '''

    #     if check_str_correct(firstName):
    #         self.firstName = firstName
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_lastName(self,lastName:str) -> bool:
    #     '''
    #         Sets the lastName of the user.
    #         Returns True if successful else False
    #         :param: `lastName` is the lastName of the user
    #     '''

    #     if check_str_correct(lastName):
    #         self.lastName = lastName
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_street(self,street:str) -> bool:
    #     '''
    #         Sets the street of the user.
    #         Returns True if successful else False
    #         :param: `street` is the street of the user
    #     '''

    #     if check_str_correct(street):
    #         self.street = street
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_houseNumber(self,houseNumber:str) -> bool:
    #     '''
    #         Sets the houseNumber of the user.
    #         Returns True if successful else False
    #         :param: `houseNumber` is the houseNumber of the user
    #     '''

    #     if check_str_correct(houseNumber):
    #         self.houseNumber = houseNumber
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_plz(self,plz:str) -> bool:
    #     '''
    #         Sets the plz of the user.
    #         Returns True if successful else False
    #         :param: `plz` is the plz of the user
    #     '''

    #     if check_str_correct(plz):
    #         self.plz = plz
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_city(self,city:str) -> bool:
    #     '''
    #         Sets the city of the user.
    #         Returns True if successful else False
    #         :param: `city` is the city of the user
    #     '''

    #     if check_str_correct(city):
    #         self.city = city
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_country(self,country:str) -> bool:
    #     '''
    #         Sets the country of the user.
    #         Returns True if successful else False
    #         :param: `country` is the country of the user
    #     '''

    #     if check_str_correct(country):
    #         self.country = country
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_rememberMe(self,rememberMe:str) -> bool:
    #     '''
    #         Sets the rememberMe of the user.
    #         Returns True if successful else False
    #         :param: `rememberMe` is the rememberMe of the user
    #     '''

    #     if check_str_correct(rememberMe):

    #         # convert rememberMe
    #         rememberMe_converted = convert_rememberMe(rememberMe)

    #         self.rememberMe = rememberMe_converted
    #         db.session.commit()
    #         return True
    #     else:
    #         return False


    # def set_full_name(self,firstName:str,lastName:str) -> bool:
    #     '''
    #         Sets the full name, lastName and firstName
    #         :param: `lastName` is the lastName of the User
    #         :param: `firstName` is the firstName of the User
    #     '''

    #     self.set_firstName(firstName)
    #     self.set_lastName(lastName)


    # def set_address(self,street:str,houseNumber:str,plz:str,city:str,country:str) -> bool:
    #     '''
    #         Sets the address including `street`, `houseNumber`, `plz`, `city`,`country`
    #         :param: `street` is the street of the user
    #         :param: `houseNumber` is the houseNumber of the user
    #         :param: `plz` is the plz of the user
    #         :param: `city` is the city of the user
    #         :param: `country` is the country of the user
    #     '''

    #     self.set_street(street)
    #     self.set_houseNumber(houseNumber)
    #     self.set_plz(plz)
    #     self.set_city(city)
    #     self.set_country(country)


    # def generate_password_reset_token(self,expiration = 600) -> str:
    #     '''
    #         generates a token to reset the passwort
    #         Returns a string
    #         :param: `expiration` is the time after which the token expires, in seconds
    #     '''
    #     if expiration <= 0:
    #         raise ValueError("Token Expiration Time can't be <= 0")

    #     return jwt.encode(
    #         {"reset_password":self.id,"exp":time() + expiration},app.config["SECRET_KEY"],algorithm="HS256"
    #     )


    # @staticmethod
    # def verify_password_reset_token(token:str) -> (User | None):
    #                                                 # this User needs the import 'from __future__ import annotations', so that a type of object User can be
    #                                                 # returned in the class User.
    #     '''
    #         verify a password reset token, if token valid return user with given id ,else return none
    #     '''
    #     try:
    #         id = jwt.decode(token,app.config["SECRET_KEY"],algorithms="HS256")["reset_password"]
    #     except:
    #         return
    #     # stmt =  select(User).where(User.id == id)
    #     # return db.session.scalar(stmt)
    #     return db.session.get(User,id)


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


    # @property
    # def password(self):
    #     raise AttributeError("Password is not a readable Attribute")


    # @password.setter
    # def password(self,password:str):
    #     self.passwort_hash = generate_password_hash(password,method = "scrypt")


    # def verifyPassword(self,password:str) -> bool:
    #     return check_password_hash(self.passwort_hash,password)


    @staticmethod
    def check_email_exists(email:str) -> bool:
        '''
            Returns True if User with this email address already exists
            :param: `email` is the Email to be checked
        '''

        if check_str_correct(email):
            # what to query
            query = select(User).where(User.email == email)
            # get result
            result = db.session.scalar(query)

            if result:
                return True
            else:
                return False


    # @property
    # def is_third_party(self) -> bool:
    #     '''
    #         Returns `True` if User with this email is third party registered.
    #         Returns `False` if not.
    #     '''
    #     return self.thirdParty if self.thirdParty else False


    @staticmethod
    def get_from_email(email:str) -> User | None:
        '''
            Returns User by given email. (staticmethod)
            :param: `email` is the email of the User
        '''

        if check_str_correct(email):
            query = select(User).where(User.email == email)
            result = db.session.scalar(query)

            return result if result else None


# class Role(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(150),unique = True)
#     users = db.relationship("User", backref = "role")


#     @staticmethod
#     def check_role_exists_by_name(role_name:str) -> bool:
#         '''
#             Checks wether the Role with the given name exists or not
#             Returns `true` or `false` 
#             :param: `role_name` is the name of the role
#         '''

#         # check if role_name is not empty str
#         if check_str_input_correct(role_name,"role_name","Role.check_role_exists_by_name"):

#             search_query = select(Role).where(Role.name == role_name)
#             result = db.session.scalar(search_query)

#             if result:
#                 return True
#             else:
#                 return False
            

#     @staticmethod
#     def get_role_by_name(role_name:str) -> Role | None:
#         '''
#             Returns a Role by given `role_name`
#             :param: `role_name` is the name of the role
#         ''' 

#         # check if role exists
#         if Role.check_role_exists_by_name(role_name):

#             query = select(Role).where(Role.name == role_name)
#             result = db.session.scalar(query)

#             return result


#class Guitar(db.Model):
    #id = db.Column(db.Integer, primary_key = True)

#what information to store:
    #Product----- Name , Price, 3d Model, Image,
    #- Color, Size, Shape, Wood,

# class Guitar(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     name = db.Column(db.String(150), unique = True)
#     price = db.Column(db.Integer)
#     stock = db.Column(db.Integer)
#     stripe_price_id = db.Column(db.String(100))
#     description = db.Column(db.Text)


    # @staticmethod
    # def check_guitar_exists(guitar:Guitar) -> bool:
    #     '''
    #         Checks whether the guitar exists in the database or not
    #         Returns a true or false
    #         :param: `guitar` is of type Guitar
    #     '''

    #     if type(guitar) != Guitar:
    #         raise TypeError("guitar should be of Type Guitar")

    #     if guitar.id == None:
    #         return False

    #     # search_query = select(Guitar).where(Guitar.id == guitar.id)
    #     # result = db.session.scalar(search_query)

    #     result = db.session.get(Guitar,guitar.id)

    #     if result:
    #         return True
    #     else:
    #         return False
        

    # @staticmethod
    # def check_guitar_exists_by_name(guitar_name:str) -> bool:
    #     '''
    #         Checks whether the guitar exists in the database or not
    #         Returns a true or false
    #         :param: `guitar_name` is the name of the guitar
    #     '''

    #     if check_str_input_correct(guitar_name,"guitar_name","check_guitar_exists_by_name"):

    #         search_query = select(Guitar).where(Guitar.name == guitar_name)
    #         result = db.session.scalar(search_query)

    #         if result:
    #             return True
    #         else:
    #             return False
            

    # @staticmethod
    # def get_by_name(guitar_name:str) -> Guitar | None:
        # '''
        #     Returns a Guitar by given `guitar_name`
        #     :param: `guitar_name` is the name of the guitar
        # ''' 

        # # check if role exists
        # if Guitar.check_guitar_exists_by_name(guitar_name):

        #     query = select(Guitar).where(Guitar.name == guitar_name)
        #     result = db.session.scalar(query)

        #     return result