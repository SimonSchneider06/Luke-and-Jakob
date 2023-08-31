import pytest
from website.models import User
from website import db

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
    assert new_user.verifyPassword("Save_Password4") == True
    assert new_user.rememberMe == True
    assert new_user.thirdParty == False
    assert new_user.role_id == customer_role.id


def test_get_order_is_None(new_user:User):
    '''
        `GIVEN` a User Model
        `WHEN` a the order gets requested, but is None
        `THEN` check if ValueError gets raised
    '''

    with pytest.raises(ValueError):
        new_user.get_order()


def test_set_order_wrong_type(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a argument of wrong type gets passed
        `THEN` check if TypeError gets raised
    '''

    wrong_type = "List"

    with pytest.raises(TypeError):
        new_user.set_order(wrong_type)


def test_set_order(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` an empty list gets passed as argument
        `THEN` check if ValueError gets raised
    '''

    empty_list = []

    with pytest.raises(ValueError):
        new_user.set_order(empty_list)


def test_user_store_order(new_user,shopping_order):
    '''
        `GIVEN` a User Model
        `WHEN` a valid order gets passed as argument
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


def test_user_generate_and_verify_token(test_app):
    '''
        `GIVEN` a User model
        `WHEN` a User generates a valid token
        `THEN` check that user gets returned
    '''

    with test_app.app_context():

        # get test User from database
        # test_user_stmt = select(User).filter_by(id = 1)
        # test_user = db.session.scalar(test_user_stmt)
        test_user = db.session.get(User,1)

        # generate token
        token = test_user.generate_password_reset_token()

        # if token real, user should be returned
        assert User.verify_password_reset_token(token) == test_user


def test_user_generate_password_reset_token_invalid_expiration(test_app):
    '''
        `GIVEN` a User model
        `WHEN` a User generates a token with invalid expiration time
        `THEN` check that Valueerror gets raised
    '''

    with test_app.app_context():

        # test_user_stmt = select(User).filter_by(id = 1)
        # test_user = db.session.scalar(test_user_stmt)
        test_user = db.session.get(User,1)

        with pytest.raises(ValueError):
            exp = -3
            test_user.generate_password_reset_token(expiration=exp)


def test_user_generate_and_verify_invalid_token(test_app):
    '''
        `GIVEN` a User model
        `WHEN` a User generates a valid token
        `THEN` check that user gets returned
    '''
     
    with test_app.app_context():
         assert User.verify_password_reset_token("i0vjejßvojfwej") == None


def test_check_user_exists(test_app):
    '''
        `GIVEN` a User method
        `WHEN` a existing user gets passed as argument
        `THEN` check if true gets returned
    '''

    with test_app.app_context():

        # get user from database
        # search_query = select(User).where(User.id == 1)
        # user = db.session.scalar(search_query)
        user = db.session.get(User,1)

        assert User.check_user_exists(user) == True


def test_check_user_exists_user_id_none(customer_role,test_app):
    '''
        `GIVEN` a User method
        `WHEN` a not existing user gets passed as argument, id = None
        `THEN` check if false gets returned
    '''

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


def test_check_user_exists_user_invalid(customer_role,test_app):
    '''
        `GIVEN` a User method
        `WHEN` a not existing user, with id gets passed as argument 
        `THEN` check if false gets returned
    '''

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


def test_check_user_exists_invalid_type(test_app):
    '''
        `GIVEN` a User method
        `WHEN` a user string gets passed as argument
        `THEN` check if TypeError gets raised
    '''

    with test_app.app_context():

        # get user from database
        user = "User"
        with pytest.raises(TypeError):
            User.check_user_exists(user)


def test_check_email_exists(new_user,test_app):
    '''
        `GIVEN` a User method
        `WHEN` a email from an existing User gets passed
        `THEN` check if True gets returned
    '''

    email = new_user.email

    with test_app.app_context():

        assert User.check_email_exists(email) == True


def test_check_email_exists_not_existing(test_app):
    '''
        `GIVEN` a User method
        `WHEN` a email from a not existing User gets passed
        `THEN` check if False gets returned
    '''

    email = "test@test.de"

    with test_app.app_context():

        assert User.check_email_exists(email) == False


def test_password_secure(test_app):
    '''
        `GIVEN` a User method
        `WHEN` a secure password gets passed
        `THEN` check if True gets returned
    '''

    password = "1Ligx;[0+32v"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    with test_app.app_context():

        assert User._check_password_secure(password) == True


def test_password_secure_not_secure(test_app):
    '''
        `GIVEN` a User method
        `WHEN` a not secure password (no punctuations) gets passed
        `THEN` check if False gets returned
    '''

    password = "1Ligx0iov32v"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    with test_app.app_context():

        assert User._check_password_secure(password) == False


def test_password_secure_to_short(test_app):
    '''
        `GIVEN` a User method
        `WHEN` a insecure password (to short) gets passed
        `THEN` check if True gets returned
    '''

    password = "1Li"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    with test_app.app_context():

        assert User._check_password_secure(password) == False


def test_check_all_user_data_correct(test_app):
    '''
        `GIVEN` a User method
        `WHEN` every input data is correct and fresh
        `THEN` check if True gets returned
    '''

    password = "1Li;o8){RA+f"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    with test_app.app_context():

        assert User.check_all_user_data_correct(
            email = "new_email@gmx.de",
            firstName = "Test",
            lastName = "lastTestName",
            houseNumber= "4a",
            street = "Teststreet",
            plz = "38923",
            city = "TestCity",
            country="TestCountry",
            password1=password,
            password2=password,
            rememberMe="on"
        ) == True


def test_check_all_user_data_correct_email_exists_already(test_app,new_user):
    '''
        `GIVEN` a User method
        `WHEN` every input data is correct, but email exists already in database
        `THEN` check if error string gets returned
    '''

    password = "1Li;o8){RA+f"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    # test_app = create_app("testing")
    with test_app.app_context():

        assert User.check_all_user_data_correct(
            email = new_user.email,
            firstName = "Test",
            lastName = "lastTestName",
            houseNumber= "4a",
            street = "Teststreet",
            plz = "38923",
            city = "TestCity",
            country="TestCountry",
            password1=password,
            password2=password,
            rememberMe="on"
        ) == "Email exists already"


def test_check_all_user_data_correct_passwords_not_matching(test_app):
    '''
        `GIVEN` a User method
        `WHEN` every input data is correct, except password 1 & 2 don't match
        `THEN` check if errorstring gets returned
    '''

    password = "1Li;o8){RA+f"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    with test_app.app_context():

        assert User.check_all_user_data_correct(
            email = "new_email@gmx.de",
            firstName = "Test",
            lastName = "lastTestName",
            houseNumber= "4a",
            street = "Teststreet",
            plz = "38923",
            city = "TestCity",
            country="TestCountry",
            password1=password,
            password2="another_password",
            rememberMe="on"
        ) == "Passwords don't match"


def test_check_all_user_data_correct_password_not_secure(test_app):
    '''
        `GIVEN` a User method
        `WHEN` every input data is correct, but password is not secure
        `THEN` check if errorstring gets returned
    '''

    password = "1Lo"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    with test_app.app_context():

        assert User.check_all_user_data_correct(
            email = "test_email@web.de",
            firstName = "Test",
            lastName = "lastTestName",
            houseNumber= "4a",
            street = "Teststreet",
            plz = "38923",
            city = "TestCity",
            country="TestCountry",
            password1=password,
            password2=password,
            rememberMe="on"
        ) == "Password not secure enough, please choose a more secure one"


def test_check_all_user_data_correct_input_not_str(test_app):
    '''
        `GIVEN` a User method
        `WHEN` every input data is correct, except one in not a string
        `THEN` check if errorstring gets returned
    '''

    password = "1Li;o8){RA+f"

    # to be secure it needs to be 
        # at least 8 character
        # have one number in it
        # have one punctuation in it
        # have an uppercase letter
        # have a lowercase letter

    with test_app.app_context():

        assert User.check_all_user_data_correct(
            email = "test_email@web.de",
            firstName = "Test",
            lastName = "lastTestName",
            houseNumber= "4a",
            street = "Teststreet",
            plz = 38923,
            city = "TestCity",
            country="TestCountry",
            password1=password,
            password2=password,
            rememberMe="on"
        ) == "Input values are not correct"


def test_convert_rememberMe_off():
    '''
        `GIVEN` a User method
        `WHEN` the value `off` is the input value
        `THEN` check if `False` gets returned
    '''

    assert User.convert_rememberMe("off") == False


def test_convert_rememberMe_on():
    '''
        `GIVEN` a User method
        `WHEN` the value `on` is the input value
        `THEN` check if `True` gets returned
    '''

    assert User.convert_rememberMe("on") == True


def test_set_firstName_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_firstName(3) == False


def test_set_lastName_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_lastName(3) == False


def test_set_street_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_street(3) == False


def test_set_houseNumber_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_houseNumber(3) == False


def test_set_plz_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_plz(3) == False


def test_set_city_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_city(3) == False


def test_set_country_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_country(3) == False


def test_set_rememberMe_no_string(new_user:User):
    '''
        `GIVEN` a User method
        `WHEN` a value, not being a string gets passed
        `THEN` check if False gets returned
    '''

    assert new_user.set_rememberMe(3) == False
