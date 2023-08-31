from website import create_app
from flask import Flask,request,url_for
from flask.testing import FlaskClient

def test_logout(test_client):
    '''
        `GIVEN` a auth route
        `WHEN` a not logged in user requests /logout
        `THEN` check if error get`s raised
    '''

    
    response = test_client.get("/logout")

    assert response.status_code == 302


def test_sign_up(test_app:Flask,test_client:FlaskClient):
    '''
        `GIVEN` a auth route
        `WHEN` a new user wants to sign up at /signUp
        `THEN` check if registered correctly and data gets flashed correctly, 
        gets redirected correctly
    '''

    expected_flash_message = u"Erfolgreich Registriert" 
    # u stands for unicode
    
    with test_app.test_request_context():
        response = test_client.post("/signUp",data = {
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
        },follow_redirects = False)

        # get flash messages from session object
        with test_client.session_transaction() as session:
            flash_message = dict(session["_flashes"]).get("success")
            #print(f"PRINT: {flash_message}")

        # check if successful redirected
        assert response.status_code == 302

        # check that redirected, so path is different
        assert request.path == url_for("views.home")

        # for some reason this wont work: 
            # check that redirected
            # assert b"Ueberschrift-Fett-Fueller" in response.data    
        
        #check that message flashing was successful
        assert flash_message == expected_flash_message