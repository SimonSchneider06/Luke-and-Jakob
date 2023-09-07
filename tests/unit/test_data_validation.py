import pytest
from website import data_validation


def test_check_str_input_correct():
    '''
        `GIVEN` a data_validation method
        `WHEN` a correct String, argument name and function gets passed 
        `THEN` check if True gets returned
    '''

    assert data_validation.check_str_input_correct("test_value","test_arg","ImageManager().check_img_ext") == True


def test_check_str_input_function_invalid():
    '''
        `GIVEN` a data_validation method
        `WHEN` a valid string, valid argument name and function, not as string, gets passed 
        `THEN` check if Error raised
    '''

    # 
    with pytest.raises(TypeError):
        data_validation.check_str_input_correct("test_string","test_arg",0)


def test_check_str_input_string_invalid():
    '''
        `GIVEN` a data_validation method
        `WHEN` a string invalid(empty or not string), argument name and function both valid strings gets passed 
        `THEN` check if Errors raised
    '''

    # not string
    with pytest.raises(TypeError):
        data_validation.check_str_input_correct(0,"test_arg","test_function")

    # empty string
    with pytest.raises(ValueError):
        data_validation.check_str_input_correct("","test_arg","test_function")


def test_check_str_input_argument_name_invalid():
    '''
        `GIVEN` a data_validation method
        `WHEN` a valid string, argument name invalid(not string and empty string) and function valid strings gets passed 
        `THEN` check if Errors raised
    '''

    # not string
    with pytest.raises(TypeError):
        data_validation.check_str_input_correct("test_string",0,"test_function")

    # empty string
    with pytest.raises(ValueError):
        data_validation.check_str_input_correct("test_string","","test_function")


def test_check_str_correct_empty_str():
    '''
        `GIVEN` a data_validation method
        `WHEN` a empty string
        `THEN` check if False gets returned
    '''

    assert data_validation.check_str_correct("") == False


def test_convert_rememberMe_off():
    '''
        `GIVEN` a data_validation method
        `WHEN` the value `off` is the input value
        `THEN` check if `False` gets returned
    '''

    assert data_validation.convert_rememberMe("off") == False


def test_convert_rememberMe_on():
    '''
        `GIVEN` a data_validation method
        `WHEN` the value `on` is the input value
        `THEN` check if `True` gets returned
    '''

    assert data_validation.convert_rememberMe("on") == True


def test_password_secure():
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

    assert data_validation.check_password_secure(password) == True


def test_password_secure_not_secure():
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

    assert data_validation.check_password_secure(password) == False


def test_password_secure_to_short():
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

    assert data_validation.check_password_secure(password) == False


def test_check_sign_in_data_correct(test_app):
    '''
        `GIVEN` a data_validation method
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

        assert data_validation.check_sign_in_data_correct(
            email = "new_email@gmx.de",
            password1=password,
            rememberMe="on"
        ) == True


def test_check_sign_in_data_correct_email_exists_already(test_app,new_user):
    '''
        `GIVEN` a data_validation method
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

        assert data_validation.check_sign_in_data_correct(
            email = new_user.email,
            password1=password,
            rememberMe="on"
        ) == "Email exists already"


def test_check_sign_in_user_data_correct_password_not_secure(test_app):
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

        assert data_validation.check_sign_in_data_correct(
            email = "new_email@gmail.com",
            password1=password,
            rememberMe="on"
        ) == "Password not secure enough, please choose a more secure one"


def test_check_sign_in_data_correct_input_not_str(test_app):
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

        assert data_validation.check_sign_in_data_correct(
            email = "",
            password1=password,
            rememberMe="on"
        ) == "Input values are not correct"