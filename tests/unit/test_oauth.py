from flask import Flask,request
import responses

from website.oauth import OAuthSignIn,GoogleSignIn


def test_OAuthSignIn_get_provider(test_app:Flask):
    '''
        :param:`GIVEN` an OAuthSignIn Method
        :param:`WHEN` an existing OAuth-Name gets passed
        :param:`THEN` check if sub-class returned correctly
    '''
    with test_app.app_context():
        assert type(OAuthSignIn.get_provider("google")) == GoogleSignIn


@responses.activate
def test_Google_get_provider_cfg(test_app:Flask,get_oauth_test_url_endpoints):
    '''
        :param:`GIVEN` an GoogleSignIn Method
        :param:`WHEN` the provider config data gets requested
        :param:`THEN` check if returned correctly
    '''
    # user a mock response, because test shouldn't depend on 3rd party 
    # things and should be fast

    with test_app.app_context():
        google_client = GoogleSignIn()

        responses.add(
            responses.GET,
            google_client.client_url,
            json = get_oauth_test_url_endpoints
        )

        assert google_client.get_provider_cfg() == get_oauth_test_url_endpoints


@responses.activate
def test_Google_get_request_uri(test_app:Flask,get_oauth_test_url_endpoints):
    '''
        :param:`GIVEN` an GoogleSignIn Method
        :param:`WHEN` the request gets passed correctly
        :param:`THEN` check if returned correctly
    '''
    # user a mock response, because test shouldn't depend on 3rd party 
    # things and should be fast

    request_uri = "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=880053595851-jsj507rb9gqvp80put9di2stq9pa8c2m.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%2F%2Fcallback%2F&scope=openid+email+profile"

    endpoint = get_oauth_test_url_endpoints["authorization_endpoint"]

    with test_app.test_request_context():
        google_client = GoogleSignIn()

        assert google_client.get_request_uri(request,endpoint) == request_uri



@responses.activate
def test_Google_get_usernifo_response(test_app:Flask,get_oauth_test_url_endpoints):
    '''
        :param:`GIVEN` an GoogleSignIn Method
        :param:`WHEN` the method gets called
        :param:`THEN` check if returned correctly
    '''
    # user a mock response, because test shouldn't depend on 3rd party 
    # things and should be fast

    json_userinfo_response = "<Response [200]>"

    endpoint = get_oauth_test_url_endpoints["userinfo_endpoint"]

    resp_header = {'Authorization': 'Bearer ya29.a0AfB_byCK2I6iIajvi7v4aJOzIniehJSl3aRsFkiAOfxYAHghDHGI9HStWmwf5U4MwjO4X414oCQ4u7we5gSl2WmFAfXr-H1qHky-X5HaYXeSA0en-oR_2hFR8duk9vNPISvLwN9CFMWNy7Nsxx15kQjB0LOL9-hkuhqZaCgYKAcUSARASFQHsvYlsDpDUlkb3QTtSqCkZ8fDMMQ0171'}

    with test_app.test_request_context():
        google_client = GoogleSignIn()
        #set token, for response later in client
        google_client.client.access_token = resp_header['Authorization']

        responses.add(
            responses.GET,
            google_client.client_url,
            json = get_oauth_test_url_endpoints
        )

        responses.add(
            responses.GET,
            "https://openidconnect.googleapis.com/v1/userinfo",
            json = json_userinfo_response, 
        )

        assert f'{google_client.get_userinfo_response(endpoint)}' == json_userinfo_response


@responses.activate
def test_Google_token_request(test_app:Flask,get_oauth_test_url_endpoints,test_client):
    '''
        :param:`GIVEN` an GoogleSignIn Method
        :param:`WHEN` the method gets called
        :param:`THEN` check if returned correctly
    '''
    # user a mock response, because test shouldn't depend on 3rd party 
    # things and should be fast

    json_userinfo_response = "<Response [200]>"

    code = "4/0Adeu5BV5YAQW9yusVk5hHzR2VLWbOi4ITscsGo2k27D5Q4PVVcQ7qJoKXxjufC5l5EVWMA"

    ssl_base_url = f"https://localhost/" # needed because oauth2 needs https

    config = get_oauth_test_url_endpoints

    token_url = "https://oauth2.googleapis.com/token"

    resp_header = {'access_token': 'ya29.a0AfB_byCK2I6iIajvi7v4aJOzIniehJSl3aRsFkiAOfxYAHghDHGI9HStWmwf5U4MwjO4X414oCQ4u7we5gSl2WmFAfXr-H1qHky-X5HaYXeSA0en-oR_2hFR8duk9vNPISvLwN9CFMWNy7Nsxx15kQjB0LOL9-hkuhqZaCgYKAcUSARASFQHsvYlsDpDUlkb3QTtSqCkZ8fDMMQ0171'}

    url_with_code = f'{ssl_base_url}?code={code}'

    with test_app.test_request_context(base_url = ssl_base_url):

        test_request = request
        test_request.url = url_with_code

        google_client = GoogleSignIn()

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

        assert f'{google_client.token_request(test_request,code,config)}' == json_userinfo_response


@responses.activate
def test_Google_authorize(test_app:Flask,get_oauth_test_url_endpoints):
    '''
        :param:`GIVEN` an GoogleSignIn Method
        :param:`WHEN` the request data is correct
        :param:`THEN` check if redirected correctly
    '''
    # user a mock response, because test shouldn't depend on 3rd party 
    # things and should be fast

    request_uri = "https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=880053595851-jsj507rb9gqvp80put9di2stq9pa8c2m.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%2F%2Fcallback%2F&scope=openid+email+profile"

    with test_app.test_request_context():
        google_client = GoogleSignIn()

        responses.add(
            responses.GET,
            google_client.client_url,
            json = get_oauth_test_url_endpoints
        )

        response = google_client.authorize(request)
        assert response.status_code == 302



@responses.activate
def test_Google_callback(test_app,get_oauth_test_url_endpoints,test_client):
    '''
        :param:`GIVEN` an GoogleSignIn Method
        :param:`WHEN` the method gets called
        :param:`THEN` check if email returned correctly
    '''
    # user a mock response, because test shouldn't depend on 3rd party 
    # things and should be fast

    code = "4/0Adeu5BV5YAQW9yusVk5hHzR2VLWbOi4ITscsGo2k27D5Q4PVVcQ7qJoKXxjufC5l5EVWMA"

    ssl_base_url = f"https://localhost/" # needed because oauth2 needs https

    token_url = "https://oauth2.googleapis.com/token"

    resp_header = {'access_token': 'ya29.a0AfB_byCK2I6iIajvi7v4aJOzIniehJSl3aRsFkiAOfxYAHghDHGI9HStWmwf5U4MwjO4X414oCQ4u7we5gSl2WmFAfXr-H1qHky-X5HaYXeSA0en-oR_2hFR8duk9vNPISvLwN9CFMWNy7Nsxx15kQjB0LOL9-hkuhqZaCgYKAcUSARASFQHsvYlsDpDUlkb3QTtSqCkZ8fDMMQ0171'}

    url_with_code = f'{ssl_base_url}?code={code}'

    email = 'Test_Email@googleOauth.de'

    json_userinfo_response = {'email': email, 'email_verified': True}

    with test_app.test_request_context(base_url = ssl_base_url):

        test_request = request
        test_request.url = url_with_code

        google_client = GoogleSignIn()

        responses.add(
            responses.GET,
            google_client.client_url,
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

        assert f'{google_client.callback(test_request)}' == email