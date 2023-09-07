from flask.testing import FlaskClient
from website.models import User
from flask import Flask
from website import db


def test_sign_up(test_client:FlaskClient,sign_up_route: str,home_route: str):
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
        "passwort1": "789LiJ;a_H",
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


def test_sign_up_wrong_data(test_client:FlaskClient,sign_up_route: str):
    '''
        `GIVEN` a auth route
        `WHEN` a new user wants to sign up at /signUp, but wrong data
        `THEN` check if redirected correctly and error message right
    '''

    expected_flash_message = b"Email exists already"

    response = test_client.post(sign_up_route,data = {
        "email":  "Max@Mustermann.de",
        "passwort1": "789LiJ;a_H",
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


def test_login(test_client:FlaskClient,new_user: User,login_route: str,home_route: str,logout_route: str):
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
        

def test_login_user_not_existing(test_client:FlaskClient,login_route: str):
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


def test_login_user_is_third_party(test_client:FlaskClient,third_party_user: User,login_route: str):
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


def test_login_password_not_matching(test_client:FlaskClient,new_user: User,login_route: str):
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


def test_logout(test_client: FlaskClient,new_user: User,login_route: str,logout_route: str):
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


def test_account(test_client:FlaskClient,new_user: User,login_route: str,account_page_route: str):
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


def test_change_user_data(test_app: Flask,test_client:FlaskClient,new_user: User,login_route: str,change_user_data_route: str,logout_route: str):
    '''
        `GIVEN` a auth route (/change_user)
        `WHEN` a user posts their new data
        `THEN` check if changed correctly
    '''

    expected_flashed_message = b"Erfolgreich Daten geaendert"

    # login user
    test_client.post(login_route, data = {
        "email": new_user.email,
        "password": "Save_Password4"
    })

    # check that rememberMe is true
    assert new_user.rememberMe == True

    response = test_client.post(change_user_data_route,data = {
        "firstName":new_user.firstName,
        "lastName": new_user.lastName,
        "street": new_user.street,
        "houseNumber":new_user.houseNumber,
        "PLZ":new_user.plz,
        "city":new_user.city,
        "selectCountry":new_user.country,
        "rememberMe":"off",
    }, follow_redirects = True)

    #check that all ok
    assert response.status_code == 200

    #check flashed message
    assert expected_flashed_message in response.data

    # check that data changed
    
    # get user from db
    with test_app.app_context():
        user = User.get_from_email(new_user.email)
    #check rememberMe got changed
    assert user.rememberMe == False


    # change rememberMe back to on
    with test_app.app_context():
        user.set_rememberMe("on")
        db.session.commit()
    
    # check that it got changed back
    assert user.rememberMe == True

    # log user out
    logout_response = test_client.get(logout_route,follow_redirects = True)
    # check that logged out
    assert b'Login' in logout_response.data


def test_change_user_data_data_wrong(login_route: str,test_client:FlaskClient,new_user: User,change_user_data_route: str):
    '''
        `GIVEN` a auth route (/change_user)
        `WHEN` a user posts their new data, which is incorrect
        `THEN` check if flash message and redirect correct
    '''

    expected_flashed_message = b"Es ist ein Fehler unterlaufen"

    # login user
    test_client.post(login_route,data = {
        "email":new_user.email,
        "password":"Save_Password4"
    },follow_redirects = True)

    response = test_client.post(change_user_data_route,data = {
        "firstName":new_user.firstName,
        "lastName": new_user.lastName,
        "street": new_user.street,
        "houseNumber":new_user.houseNumber,
        "PLZ":new_user.plz,
        "city":new_user.city,
        "selectCountry":"",
        "rememberMe":"off",
    }, follow_redirects = True)

    #check that all ok
    assert response.status_code == 200

    # check that on same page
    assert response.request.path == change_user_data_route

    #check flashed message
    assert expected_flashed_message in response.data


def test_password_reset_user_logged_in(password_reset_route: str,test_client:FlaskClient,log_user_in: None,home_route: str):
    '''
        `GIVEN` an auth route
        `WHEN` a currently logged in user requests it
        `THEN` check if redirected to home page
    '''  
    # logging the user in
    log_user_in

    # requesting the password_reset_route
    response = test_client.get(password_reset_route,follow_redirects = True)

    assert response.status_code == 200

    assert response.request.path == home_route

    assert b"Ueberschrift-Fett-Fueller" in response.data


def test_password_reset(test_client: FlaskClient,password_reset_route: str, new_user: User,login_route: str):
    '''
        :param:`GIVEN` an auth route
        :param:`WHEN` a not logged in user makes post request
        :param:`THEN` check if flash message and redirect are correct
    ''' 

    expected_flash_message = b"Ihnen wurde eine Email gesendet"

    response = test_client.post(password_reset_route,data = {
        "email":new_user.email
    }, follow_redirects = True)

    # check response code, flash message and redirect
    assert response.status_code == 200
    assert response.request.path == login_route
    assert expected_flash_message in response.data


def test_password_reset_get(test_client: FlaskClient,password_reset_route: str):
    '''
        :param:`GIVEN` an auth route
        :param:`WHEN` a not logged in user requests it
        :param:`THEN` check if flash message and redirect are correct
    ''' 

    response = test_client.get(password_reset_route)

    assert response.status_code == 200
    assert b'Bitte geben Sie hier Ihre Email Addresse ein' in response.data


def test_new_password(test_client: FlaskClient,test_app: Flask,new_password_route: str):
    '''
        :param:`GIVEN` an auth route
        :param:`WHEN` a not logged in user requests it, with a valid token
        :param:`THEN` check if site successfully loaded
    ''' 

    # generate token
    with test_app.app_context():
        
        # this doesn't work because new_user doesn't have an ID
        #token = new_user.generate_password_reset_token()

        user = db.session.get(User,1)
        token = user.generate_password_reset_token()

    # get full route
    
    route = new_password_route(token)
    #print(f'Route: {route}')
    response = test_client.get(route)
        
    #response = test_client.get(route)

    #check if status code ok and still on this site
    assert response.status_code == 200
    assert b'Passwort Zur' in response.data
    assert response.request.path == route


def test_new_password_post(test_client: FlaskClient,test_app: Flask,new_password_route: str,home_route:str):
    '''
        :param:`GIVEN` an auth route
        :param:`WHEN` a not logged in user posts a new password with a valid token
        :param:`THEN` check if password changed, flash message right, redirect right
    ''' 

    expected_flash_message = b"Ihr Passwort wurde erfolgreich"

    old_password = "Save_Password4"

    new_test_password = "New_MoreSe+ure4"

    # generate token
    with test_app.app_context():

        user = db.session.get(User,1)
        token = user.generate_password_reset_token()

    # check password of user is "Save_Password4"
    assert user.verifyPassword(old_password) == True

    route = new_password_route(token)

    with test_app.app_context():

        response = test_client.post(route,data = {
            "password1":new_test_password,
            "password2":new_test_password
        },follow_redirects = True)

    # check response status code, redirect, flash message
    assert response.status_code == 200
    assert response.request.path == home_route
    assert expected_flash_message in response.data

    #check new password
    
    # doesn't work without getting the user a second time
    # i think the problem lies, that the user doesn't get updated
    # when the password gets changed, so you need to get the user 
    # a second time to check if password got changed
    # assert user.verifyPassword(new_test_password) == True

    # get user
    with test_app.app_context():
        user = db.session.get(User,1)
    # check password got changed
    assert user.verifyPassword(new_test_password) == True

    # change password back to old one
    user.password = old_password

    with test_app.app_context():
        db.session.commit()

    #check that changed
    assert user.verifyPassword(old_password) == True


def test_new_password_post_token_invalid(test_client: FlaskClient,new_password_route: str,home_route:str):
    '''
        :param:`GIVEN` an auth route
        :param:`WHEN` a not logged in user requests this route with an invalid token
        :param:`THEN` check if redirected back to homepage
    ''' 

    invalid_token = "this_token_is_invalid_02vh9s0v"
    route = new_password_route(invalid_token)

    response = test_client.get(route,follow_redirects = True)

    # check status code and webpage
    assert response.status_code == 200
    assert response.request.path == home_route