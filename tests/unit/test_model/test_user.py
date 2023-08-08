import pytest
from website.models import User
from website import create_app,db
from sqlalchemy import select

def test_new_user_data_correct(new_user,customer_role):
    '''
        `GIVEN` a User Model
        `WHEN` a new User is created
        `THEN` check the fields email, firstName, lastName, street,
        houseNumber, plz, city, country, password_hash, rememberMe, date_added,
        thirdParty, order, role_id are defined correctly
    '''

    assert new_user.email == "schneider_berghausen@web.de"
    assert new_user.firstName == "Simon"
    assert new_user.lastName == "Schneider"
    assert new_user.street == "Zum Wacholdertal"
    assert new_user.houseNumber == "1"
    assert new_user.plz == "93336"
    assert new_user.city == "Altmannstein"
    assert new_user.country == "Deutschland"
    assert new_user.verifyPassword("Save_Password") == True
    assert new_user.rememberMe == True
    assert new_user.thirdParty == False
    assert new_user.role_id == customer_role.id


def test_user_store_order(new_user,shopping_order):
    '''
        `GIVEN` a User Model
        `WHEN` a User buys something the order is stored in the database
        `THEN` check if stored correctly
    '''

    new_user.set_order(shopping_order)
    assert new_user.get_order() == shopping_order


def test_user_read_password(new_user):
    '''
        `GIVEN` a User Password
        `WHEN` a someone wants to read it
        `THEN` check if attributeError gets raised
    '''

    with pytest.raises(AttributeError):
        new_user.password


def test_user_generate_and_verify_token():
    '''
        `GIVEN` a User model
        `WHEN` a User generates a valid token
        `THEN` check that user gets returned
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        # get test User from database
        # test_user_stmt = select(User).filter_by(id = 1)
        # test_user = db.session.scalar(test_user_stmt)
        test_user = db.session.get(User,1)

        # generate token
        token = test_user.generate_password_reset_token()

        # if token real, user should be returned
        assert User.verify_password_reset_token(token) == test_user


def test_user_generate_password_reset_token_invalid_expiration():
    '''
        `GIVEN` a User model
        `WHEN` a User generates a token with invalid expiration time
        `THEN` check that Valueerror gets raised
    '''
    test_app = create_app("testing")
    with test_app.app_context():

        # test_user_stmt = select(User).filter_by(id = 1)
        # test_user = db.session.scalar(test_user_stmt)
        test_user = db.session.get(User,1)

        with pytest.raises(ValueError):
            exp = -3
            test_user.generate_password_reset_token(expiration=exp)


def test_user_generate_and_verify_invalid_token():
    '''
        `GIVEN` a User model
        `WHEN` a User generates a valid token
        `THEN` check that user gets returned
    '''
     
    test_app = create_app("testing")
    with test_app.app_context():
         assert User.verify_password_reset_token("i0vjejßvojfwej") == None


def test_check_user_exists():
    '''
        `GIVEN` a User method
        `WHEN` a existing user gets passed as argument
        `THEN` check if true gets returned
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        # get user from database
        # search_query = select(User).where(User.id == 1)
        # user = db.session.scalar(search_query)
        user = db.session.get(User,1)

        assert User.check_user_exists(user) == True


def test_check_user_exists_user_id_none(customer_role):
    '''
        `GIVEN` a User method
        `WHEN` a not existing user gets passed as argument, id = None
        `THEN` check if false gets returned
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        # get user 
        user = User(
            email = "test@web.de",
            firstName = "Test",
            lastName = "Test",
            street = "Test-Street",
            houseNumber = "1",
            plz = "23533",
            city = "Altmannstein",
            country = "Deutschland",
            password = "Save_Password",
            rememberMe = True,
            thirdParty = False,
            role = customer_role
        )

        assert User.check_user_exists(user) == False


def test_check_user_exists_user_invalid(customer_role):
    '''
        `GIVEN` a User method
        `WHEN` a not existing user, with id gets passed as argument 
        `THEN` check if false gets returned
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        # get user 
        user = User(
            id = 6,
            email = "test@web.de",
            firstName = "Test",
            lastName = "Test",
            street = "Test-Street",
            houseNumber = "1",
            plz = "23533",
            city = "Altmannstein",
            country = "Deutschland",
            password = "Save_Password",
            rememberMe = True,
            thirdParty = False,
            role = customer_role
        )

        assert User.check_user_exists(user) == False


def test_check_user_exists_invalid_type():
    '''
        `GIVEN` a User method
        `WHEN` a existing user gets passed as argument
        `THEN` check if TypeError gets raised
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        # get user from database
        user = "User"
        with pytest.raises(TypeError):
            User.check_user_exists(user)