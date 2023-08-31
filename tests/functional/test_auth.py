from flask import Flask,url_for
from flask.testing import FlaskClient


def test_sign_up(test_client:FlaskClient,sign_up_route,home_route):
    '''
        `GIVEN` a auth route
        `WHEN` a new user wants to sign up at /signUp
        `THEN` check if registered correctly and data gets flashed correctly, 
        gets redirected correctly
    '''

    expected_flash_message = b"Erfolgreich Registriert" 
    # u stands for unicode

    response = test_client.post(sign_up_route,data = {
        "email":  "Max@Mustermann.de",
        "firstName": "Max",
        "lastName": "Mustermann",
        "street": "Teststraße",
        "houseNumber":"14c",
        "PLZ":"87638",
        "city":"Frankfurt",
        "selectCountry":"Germany",
        "passwort1": "789LiJ;a_H",
        "passwort2": "789LiJ;a_H",
        "rememberMe": "on",
    },follow_redirects = True)

    # get flash messages from session object
    # with test_client.session_transaction() as session:
    #     flash_message = dict(session["_flashes"]).get("success")
        #print(f"PRINT: {flash_message}")

    # check if successful redirected
    assert response.status_code == 200

    # check that redirected, so path is different
    assert response.request.path == home_route

    # check that redirected
    assert b"Ueberschrift-Fett-Fueller" in response.data    
    
    #check that message flashing was successful
    assert expected_flash_message in response.data


def test_sign_up_wrong_data(test_client:FlaskClient,sign_up_route):
    '''
        `GIVEN` a auth route
        `WHEN` a new user wants to sign up at /signUp, but wrong data
        `THEN` check if redirected correctly and error message right
    '''

    expected_flash_message = b"Email exists already"

    response = test_client.post(sign_up_route,data = {
        "email":  "Max@Mustermann.de",
        "firstName": "Max",
        "lastName": "Mustermann",
        "street": "Teststraße",
        "houseNumber":"14c",
        "PLZ":"87638",
        "city":"Frankfurt",
        "selectCountry":"Germany",
        "passwort1": "789LiJ;a_H",
        "passwort2": "789LiJ;a_H",
        "rememberMe": "on",
    }, follow_redirects = True)

    # with test_client.session_transaction() as session:
        # flash_message = dict(session["_flashes"]).get("error")

    # check that all ok
    assert response.status_code == 200

    # check if flash_message is expected message
    assert expected_flash_message in response.data

    # check if still same page
    assert response.request.path == sign_up_route


def test_login(test_client:FlaskClient,new_user,login_route,home_route,logout_route):
    '''
        `GIVEN` a auth route
        `WHEN` a user wants to login at /login
        `THEN` check if logged in correctly and redirected
    '''

    expected_flash_message = b'Erfolgreich Angemeldet'


    response = test_client.post(login_route,data = {
        "email": new_user.email,
        "password": "Save_Password4"
    }, follow_redirects = True)

    # check that all ok
    assert response.status_code == 200

    # check flash message
    assert expected_flash_message in response.data

    # check for redirect
    assert response.request.path == home_route
    assert b'Ueberschrift-Fett-Fueller' in response.data

    # check if logged in by using navbar
    assert b'Account' in response.data

    #logging out the user, to make tests not dependent on each other
    test_client.get(logout_route)
        

def test_login_user_not_existing(test_client:FlaskClient,login_route):
    '''
        `GIVEN` a auth route
        `WHEN` a user wants to login at /login
        `THEN` check if logged in correctly and redirected
    '''

    expected_flash_message = b"Email existiert nicht"

    response = test_client.post(login_route,data = {
        "email":"not_existing@gmail.com",
        "password":"1234589z2"
    },follow_redirects = True)

    # check response code
    assert response.status_code == 200
    
    # check flash message
    assert expected_flash_message in response.data

    # check that redirected to auth.login
    assert response.request.path == login_route


def test_login_user_is_third_party(test_client:FlaskClient,third_party_user,login_route):
    '''
        `GIVEN` a auth route
        `WHEN` a user wants to login at /login, but he has registered using a 3rd party service
        `THEN` check if flash message and redirect are correct
    '''

    expected_flash_message = b"Sie haben sich ueber einen Drittanbieter registriert"

    response = test_client.post(login_route,data = {
        "email":third_party_user.email,
        "password":None
    },follow_redirects = True)

    # check response code
    assert response.status_code == 200
    
    # check flash message
    assert expected_flash_message in response.data

    # check that redirected to auth.login
    assert response.request.path == login_route


def test_login_password_not_matching(test_client:FlaskClient,new_user,login_route):
    '''
        `GIVEN` a auth route
        `WHEN` a user wants to login at /login, password not correct
        `THEN` check if flash message and redirect are correct
    '''

    expected_flash_message = b"Passwort ist Falsch"

    response = test_client.post(login_route,data = {
        "email":new_user.email,
        "password":"Wrong_password"
    },follow_redirects = True)

    # check response code
    assert response.status_code == 200
    
    # check flash message
    assert expected_flash_message in response.data

    # check that redirected to auth.login
    assert response.request.path == login_route


def test_logout(test_client,new_user,login_route,logout_route):
    '''
        `GIVEN` a auth route
        `WHEN` a logged in user requests /logout
        `THEN` check if gets logged out
    '''
    # log user in, so it can be logged out again
    response_before_test = test_client.post(login_route, data = {
        "email": new_user.email,
        "password": "Save_Password4"
    },follow_redirects = True)

    assert b'Account' in response_before_test.data

    # logging out the user, from the above function
    response = test_client.get(logout_route,follow_redirects = True)

    # check status code
    assert response.status_code == 200

    #check that redirect worked
    assert response.request.path == login_route

    #check if not logged in by using navbar
    assert b'Login' in response.data


def test_account(test_client:FlaskClient,new_user,login_route,account_page_route):
    '''
        `GIVEN` a auth route (/account) and a logged in user
        
        `WHEN` that route gets requested
        
        `THEN` check
    '''

    # login user
    test_client.post(login_route, data = {
        "email": new_user.email,
        "password": "Save_Password4"
    })

    # get account page
    response = test_client.get(account_page_route)

    # check if status code ok
    assert response.status_code == 200

    # check page got accessed
    assert b"Mein Konto" in response.data
    assert b'Allgemeine Informationen' in response.data

    # check data correct
    assert bytes(new_user.firstName, encoding="utf-8") in response.data
    assert bytes(new_user.email, encoding = "utf-8") in response.data
    assert bytes(new_user.country, encoding = "utf-8") in response.data


def test_change_user_data(test_client:FlaskClient,new_user,login_route,change_user_data_route):
    '''
        `GIVEN` a auth route (/change_user)
        `WHEN` a user posts their new data
        `THEN` check if changed correctly
    '''

    # login user
    test_client.post(login_route, data = {
        "email": new_user.email,
        "password": "Save_Password4"
    })

    response = test_client.post(change_user_data_route,data = {
        
    })