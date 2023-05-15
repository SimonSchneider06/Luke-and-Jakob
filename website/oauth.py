import requests
from flask import current_app as app
from oauthlib.oauth2 import  WebApplicationClient
import json
# for oauth login check https://realpython.com/flask-google-login/
# and https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask


class OAuthSignIn(object):
    providers = None

    def __init__(self,provider_name):
        self.provider_name = provider_name
        credentials = app.config["OAUTH_CREDENTIALS"][self.provider_name]
        self.client_id = credentials["id"]
        self.client_secret = credentials["secret"]
        self.client_url = credentials["url"]
        self.client = WebApplicationClient(self.client_id)

    #get client config
    def get_provider_cfg(self):
        return requests.get(self.client_url).json()
    
    #get request url
    def get_request_uri(self,request):
        #get enpoint for data
        provider_cfg = self.get_provider_cfg()
        authorization_endpoint = provider_cfg["authorization_endpoint"]

        #construct provider login request and provide scopes for getting the data
        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri= request.base_url + f"/callback/",
            scope = ["openid", "email", "profile"]
        )
        return request_uri
    
    def get_token_endpoint(self):
        #get token endpoint
        provider_cfg = self.get_provider_cfg()
        token_endpoint = provider_cfg["token_endpoint"]

        return token_endpoint
    
    def get_userinfo_response(self):
        provider_cfg = self.get_provider_cfg()
        userinfo_endpoint = provider_cfg["userinfo_endpoint"]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data = body)

        return userinfo_response
    
    def token_request(self,request,code):
        
        #get token endpoint
        token_endpoint = self.get_token_endpoint()

        #prepare and send request to get tokens
        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url= request.base_url,
            code = code
        )

        #get response from google
        token_response = requests.post(
            token_url,
            headers = headers,
            data = body,
            auth = (self.client_id, self.client_secret)
        )

        #Parse the token
        self.client.parse_request_body_response(json.dumps(token_response.json()))

        # get endpoint for userinfo
        userinfo_response = self.get_userinfo_response()

        return userinfo_response