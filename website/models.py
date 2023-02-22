from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#------------user and roles--------------------------

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True)
    name = db.Column(db.String(200))
    telNumber = db.Column(db.Integer)
    alter = db.Column(db.Integer)
    passwort = db.Column(db.String(200))
    date_added = db.Column(db.DateTime(timezone = True),default = func.now())
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))


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