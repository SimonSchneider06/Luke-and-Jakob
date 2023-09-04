from __future__ import annotations
from flask import Flask,url_for
from typing import Iterable

from website import db,create_app

from website.models import User,Guitar,Role

class TestDatabaseSetup:

    '''
        Does the Database Setup
    '''

    @staticmethod
    def database_setup(test_app:Flask,test_data:Iterable[Role|User|Guitar]) -> None:
        '''
            Inserts the data into the database
            Database Setup
            :param: `test_app` is the Flask app for testing
            :param: `test_data` is the test_data, containing of Users, Roles and/or Guitars 

        '''


        with test_app.app_context():

            db.create_all()

            db.session.add_all(test_data)
            
            db.session.commit()


    @staticmethod
    def database_teardown(test_app:Flask) -> None:
        '''
            Teardown the old database
            :param: `test_app` is a Flask test app
        '''

        with test_app.app_context():
            db.session.remove()
            db.drop_all()


class TestDataSetup:

    def create_user(self,customer_role:Role) -> User:
            '''
            Create and return a new, valid user with Role Customer
            :param: `customer_role` is the Role of the User
            '''
            user = User(
                email = "schneider_berghausen@web.de",
                firstName = "Simon",
                lastName = "Schneider",
                street = "Zum Wacholdertal",
                houseNumber = "1",
                plz = "93336",
                city = "Altmannstein",
                country = "Deutschland",
                password = "Save_Password4",
                rememberMe = True,
                thirdParty = False,
                role = customer_role
            )
                
            return user
    

    def create_admin_user(self,admin_role:Role) -> User:
            '''
            Create and return a new, valid user with Role Admin
            :param: `admin_role` is the Role of the User
            '''
            user = User(
                email = "simon@jacksn.de",
                firstName = "Simon",
                lastName = "Schneider",
                street = "Zum Wacholdertal",
                houseNumber = "1",
                plz = "93336",
                city = "Altmannstein",
                country = "Deutschland",
                password = "PW_;Save42",
                rememberMe = True,
                thirdParty = False,
                role = admin_role
            )
                
            return user


    def create_admin_role(self) -> Role:
        '''
            Returns the admin role
        '''
        role = Role(name = "Admin")
        return role


    def create_customer_role(self) -> Role:
        '''
            Returns the customer role
        '''
        role = Role(name = "Customer")
        return role


    def create_guitar(self) -> Guitar:
        '''
            Create a new Guitar
        '''
        guitar = Guitar(
            name = "Test",
            price = 1500,
            stock = 5,
            stripe_price_id = "price_1N4QMpGKMAM99iKsPRgqFrgU",
            description = "Die Perfekte Gitarre für Anfänger bis Profi"
        )

        return guitar
    

    def create_third_party_user(self,customer_role:Role) -> User:
        '''
            Create user who registered through 3rd party
            :param: `customer_role` is the Role with name "Customer"
        '''

        # no other data, because 3rd party doesn't get more data from google
        user = User(
                email = "thirdParty@gmail.com",
                firstName = "TestThird",
                lastName = "TestParty",
                thirdParty = True,
                role = customer_role
            )
                
        return user


    def create_all_test_data(self) -> list[Role | User | Guitar]:
        '''
            Runns all methods of this class and returns all TestData
        '''

        customer_role = self.create_customer_role()
        admin_role = self.create_admin_role()
        user = self.create_user(customer_role)
        admin_user = self.create_admin_user(admin_role)
        third_party_user = self.create_third_party_user(customer_role)
        guitar = self.create_guitar()

        data = [customer_role,admin_role,user,third_party_user,guitar,admin_user]

        return data
        

class TestAppSetup:
    '''
        Complete Setup for the testing Application
    '''

    @staticmethod
    def create_test_app():
        '''
            Returns the test app
        '''

        test_app = create_app("testing")
        return test_app
    

class RouteSetup:
    '''
        Returns the routes of each page
    '''

    @staticmethod
    def get_route_by_name(test_app:Flask,route_name:str,**kwargs):
        '''
            Returns the route by the given name
            :param: `route_name` is the function name in the blueprint, e.g. auth.sign_up
            :param: `test_app` is the flask app
            :param: `**kwargs` is all the keyword arguments, which may be nessecary for the route, like a variable
            like <product_name>
        '''

        with test_app.test_request_context():

            route = url_for(route_name,**kwargs)

        return route