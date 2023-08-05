import pytest
from flask import Flask

from website.models import User,Role,Guitar 
from website import create_app
from website import db
    


@pytest.fixture(scope = "module")
def admin_role() -> Role:
    '''
        Returns the admin role
    '''
    role = Role(name = "Admin")
    return role


@pytest.fixture(scope = "module")
def customer_role() -> Role:
    '''
        Returns the customer role
    '''
    role = Role(name = "Customer")
    return role


@pytest.fixture(scope = "module")
def new_user(customer_role:callable) -> User:
    '''
        Create a new, valid user
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
        password = "Save_Password",
        rememberMe = True,
        thirdParty = False,
        role = customer_role
    )
        
    return user

@pytest.fixture(scope = "function")
def shopping_order() -> list[dict]:
    '''
        Create a shopping order
    '''

    order = [{"id":1,"quantity":1}]

    return order

@pytest.fixture(scope = "module")
def new_guitar() -> Guitar:
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

# needed to setup database
# @pytest.fixture(scope="module")
# def insert_data_to_database(new_guitar,new_user,customer_role,admin_role):
#     '''
#         Inserts the data into the database
#     '''

#     test_app = create_app("testing")
#     with test_app.app_context():

#         db.session.add(new_guitar)
#         db.session.add(new_user)
#         db.session.add(admin_role)
#         db.session.add(customer_role)
#         db.session.commit()