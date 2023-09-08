from flask.testing import FlaskClient
from flask import Flask
import responses

from website import db
from website.models import User

def test_oauth_login_user_already_logged_in(login_test_client:FlaskClient,oauth_login_route,home_route):
    '''
        :param:`GIVEN` an oauth_route
        :param:`WHEN` an already logged in user requests it
        :param:`THEN` check if redirected to homepage
    '''

    route = oauth_login_route("google")

    response = login_test_client.post(route,data = {},follow_redirects = True)

    assert response.status_code == 200
    assert response.request.path == home_route


@responses.activate
def test_oauth_login_new_user(test_app:Flask,test_client:FlaskClient,oauth_login_route,get_oauth_test_url_endpoints):
    '''
        :param:`GIVEN` an oauth_route
        :param:`WHEN` a new user requests it
        :param:`THEN` check if status code correct
    '''

    route = oauth_login_route("google")

    with test_app.test_request_context():
        google_client_url = test_app.config["OAUTH_CREDENTIALS"]["google"]["url"]

        responses.add(
                responses.GET,
                google_client_url,
                json = get_oauth_test_url_endpoints
            )

        response = test_client.post(route,data = {})

    # external redirect not supported
    assert response.status_code == 302


def test_oauth_callback_user_already_logged_in(login_test_client:FlaskClient,oauth_callback_route,home_route):
    '''
        :param:`GIVEN` an oauth_route
        :param:`WHEN` an already logged in user requests it
        :param:`THEN` check if redirected to homepage
    '''

    route = oauth_callback_route("google")

    response = login_test_client.get(route,follow_redirects = True)

    assert response.status_code == 200
    assert response.request.path == home_route


@responses.activate
def test_oauth_callback_email_not_verified(test_app:Flask,test_client:FlaskClient,oauth_callback_route,get_oauth_test_url_endpoints):
    '''
        :param:`GIVEN` an oauth_route
        :param:`WHEN` an user, where email isn't verified requests it
        :param:`THEN` check if flash message and status code correct
    '''

    expected_flash_message = b"User email not available or not verified by google"

    route = oauth_callback_route("google")

    code = "4/0Adeu5BV5YAQW9yusVk5hHzR2VLWbOi4ITscsGo2k27D5Q4PVVcQ7qJoKXxjufC5l5EVWMA"

    ssl_base_url = f"https://localhost/" # needed because oauth2 needs https

    token_url = "https://oauth2.googleapis.com/token"

    resp_header = {'access_token': 'ya29.a0AfB_byCK2I6iIajvi7v4aJOzIniehJSl3aRsFkiAOfxYAHghDHGI9HStWmwf5U4MwjO4X414oCQ4u7we5gSl2WmFAfXr-H1qHky-X5HaYXeSA0en-oR_2hFR8duk9vNPISvLwN9CFMWNy7Nsxx15kQjB0LOL9-hkuhqZaCgYKAcUSARASFQHsvYlsDpDUlkb3QTtSqCkZ8fDMMQ0171'}

    route_with_code = f'{route}?code={code}'

    email = 'Test_Email@googleOauth.de'

    json_userinfo_response = {'email': email, 'email_verified': False}

    with test_app.test_request_context(base_url = ssl_base_url):

        google_client_url = test_app.config["OAUTH_CREDENTIALS"]["google"]["url"]

        responses.add(
            responses.GET,
            google_client_url,
            json = get_oauth_test_url_endpoints
        )

        responses.add(
            responses.POST,
            token_url,
            json = resp_header,
        )

        responses.add(
            responses.GET,
            "https://openidconnect.googleapis.com/v1/userinfo",
            json = json_userinfo_response, 
        )

        response = test_client.get(route_with_code,base_url = ssl_base_url)

        assert response.status_code == 400
        assert expected_flash_message in response.data


@responses.activate
def test_oauth_callback_email_verified_user_not_existing(test_app:Flask,test_client:FlaskClient,oauth_callback_route,get_oauth_test_url_endpoints,home_route):
    '''
        :param:`GIVEN` an oauth_route
        :param:`WHEN` an new user requests it
        :param:`THEN` check if flash message and status code correct
    '''

    expected_flash_message = b"Sie haben sich erfolgreich registriert"

    route = oauth_callback_route("google")

    code = "4/0Adeu5BV5YAQW9yusVk5hHzR2VLWbOi4ITscsGo2k27D5Q4PVVcQ7qJoKXxjufC5l5EVWMA"

    ssl_base_url = f"https://localhost/" # needed because oauth2 needs https

    token_url = "https://oauth2.googleapis.com/token"

    resp_header = {'access_token': 'ya29.a0AfB_byCK2I6iIajvi7v4aJOzIniehJSl3aRsFkiAOfxYAHghDHGI9HStWmwf5U4MwjO4X414oCQ4u7we5gSl2WmFAfXr-H1qHky-X5HaYXeSA0en-oR_2hFR8duk9vNPISvLwN9CFMWNy7Nsxx15kQjB0LOL9-hkuhqZaCgYKAcUSARASFQHsvYlsDpDUlkb3QTtSqCkZ8fDMMQ0171'}

    route_with_code = f'{route}?code={code}'

    email = 'Test_Email@googleOauth.de'

    json_userinfo_response = {'email': email, 'email_verified': True}

    with test_app.test_request_context(base_url = ssl_base_url):

        google_client_url = test_app.config["OAUTH_CREDENTIALS"]["google"]["url"]

        responses.add(
            responses.GET,
            google_client_url,
            json = get_oauth_test_url_endpoints
        )

        responses.add(
            responses.POST,
            token_url,
            json = resp_header,
        )

        responses.add(
            responses.GET,
            "https://openidconnect.googleapis.com/v1/userinfo",
            json = json_userinfo_response, 
        )

        response = test_client.get(route_with_code,base_url = ssl_base_url,follow_redirects = True)

        assert response.status_code == 200
        assert expected_flash_message in response.data
        assert response.request.path == home_route

        # delete user again
        user = User.get_from_email(email)
        db.session.delete(user)
        db.session.commit()


@responses.activate
def test_oauth_callback_email_verified_user_is_third_party(test_app:Flask,test_client:FlaskClient,oauth_callback_route,get_oauth_test_url_endpoints,home_route,third_party_user):
    '''
        :param:`GIVEN` an oauth_route
        :param:`WHEN` an existing user,who is already registered requests it
        :param:`THEN` check if flash message and status code correct
    '''

    expected_flash_message = b"Sie haben sich erfolgreich eingeloggt"

    route = oauth_callback_route("google")

    code = "4/0Adeu5BV5YAQW9yusVk5hHzR2VLWbOi4ITscsGo2k27D5Q4PVVcQ7qJoKXxjufC5l5EVWMA"

    ssl_base_url = f"https://localhost/" # needed because oauth2 needs https

    token_url = "https://oauth2.googleapis.com/token"

    resp_header = {'access_token': 'ya29.a0AfB_byCK2I6iIajvi7v4aJOzIniehJSl3aRsFkiAOfxYAHghDHGI9HStWmwf5U4MwjO4X414oCQ4u7we5gSl2WmFAfXr-H1qHky-X5HaYXeSA0en-oR_2hFR8duk9vNPISvLwN9CFMWNy7Nsxx15kQjB0LOL9-hkuhqZaCgYKAcUSARASFQHsvYlsDpDUlkb3QTtSqCkZ8fDMMQ0171'}

    route_with_code = f'{route}?code={code}'

    email = third_party_user.email

    json_userinfo_response = {'email': email, 'email_verified': True}

    with test_app.test_request_context(base_url = ssl_base_url):

        google_client_url = test_app.config["OAUTH_CREDENTIALS"]["google"]["url"]

        responses.add(
            responses.GET,
            google_client_url,
            json = get_oauth_test_url_endpoints
        )

        responses.add(
            responses.POST,
            token_url,
            json = resp_header,
        )

        responses.add(
            responses.GET,
            "https://openidconnect.googleapis.com/v1/userinfo",
            json = json_userinfo_response, 
        )

        response = test_client.get(route_with_code,base_url = ssl_base_url,follow_redirects = True)

        assert response.status_code == 200
        assert expected_flash_message in response.data
        assert response.request.path == home_route


@responses.activate
def test_oauth_callback_email_verified_user_not_third_party(test_app:Flask,test_client:FlaskClient,oauth_callback_route,get_oauth_test_url_endpoints,home_route,new_user):
    '''
        :param:`GIVEN` an oauth_route
        :param:`WHEN` an existing user,who is already registered,but not through 3rd party requests it
        :param:`THEN` check if flash message and status code correct
    '''

    expected_flash_message = b"Diese Email ist bereits unter einem normalen Account angemeldet"

    route = oauth_callback_route("google")

    code = "4/0Adeu5BV5YAQW9yusVk5hHzR2VLWbOi4ITscsGo2k27D5Q4PVVcQ7qJoKXxjufC5l5EVWMA"

    ssl_base_url = f"https://localhost/" # needed because oauth2 needs https

    token_url = "https://oauth2.googleapis.com/token"

    resp_header = {'access_token': 'ya29.a0AfB_byCK2I6iIajvi7v4aJOzIniehJSl3aRsFkiAOfxYAHghDHGI9HStWmwf5U4MwjO4X414oCQ4u7we5gSl2WmFAfXr-H1qHky-X5HaYXeSA0en-oR_2hFR8duk9vNPISvLwN9CFMWNy7Nsxx15kQjB0LOL9-hkuhqZaCgYKAcUSARASFQHsvYlsDpDUlkb3QTtSqCkZ8fDMMQ0171'}

    route_with_code = f'{route}?code={code}'

    email = new_user.email

    json_userinfo_response = {'email': email, 'email_verified': True}

    with test_app.test_request_context(base_url = ssl_base_url):

        google_client_url = test_app.config["OAUTH_CREDENTIALS"]["google"]["url"]

        responses.add(
            responses.GET,
            google_client_url,
            json = get_oauth_test_url_endpoints
        )

        responses.add(
            responses.POST,
            token_url,
            json = resp_header,
        )

        responses.add(
            responses.GET,
            "https://openidconnect.googleapis.com/v1/userinfo",
            json = json_userinfo_response, 
        )

        response = test_client.get(route_with_code,base_url = ssl_base_url,follow_redirects = True)

        assert response.status_code == 200
        assert expected_flash_message in response.data
        assert response.request.path == home_route