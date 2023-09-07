from __future__ import annotations

import requests
from requests import Response

from flask import current_app as app
from flask import redirect
from flask.wrappers import Request
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


    def authorize(self,request:Request):
        pass    #pragma: no cover


    def callback(self,request:Request):
        pass    #pragma: no cover


    @classmethod
    def get_provider(self,provider_name:str) -> OAuthSignIn:
        '''
            Returns the Class of the provider with the given Name
            The Returned Class is a SubClass of OAuthSignIn
            :param: `provider_name` is the name of the provider
        '''
        
        if self.providers is None:
            self.providers = {}

            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider

        return self.providers[provider_name]


class GoogleSignIn(OAuthSignIn):

    def __init__(self):
        super(GoogleSignIn,self).__init__("google")
        self.client = WebApplicationClient(self.client_id)


    def get_provider_cfg(self):
        '''
            Requests the client url and returns the provider_config data in json format
        '''
        provider_cfg = requests.get(self.client_url).json()
        return provider_cfg
    
    
    def get_request_uri(self,request:Request,authorization_endpoint:str):
        '''
            Returns the request url for the login process
            :param: `request` is of type `Request` from flask.wrappers, to construct the base url
            :param: `authorization_endpoint` is the endpoint url for the authorization
        '''

        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri= request.base_url + f"/callback/",
            scope = ["openid", "email", "profile"]
        )

        return request_uri
    

    def get_userinfo_response(self,userinfo_endpoint:str) -> Response:
        '''
            Returns the userinfo response
            :param: `userinfo_endpoint` is the url for the endpoint
        '''
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data = body)

        return userinfo_response
    

    def token_request(self,request,code:str,config:dict[str , str]) -> Response:
        
        #get token endpoint
        token_endpoint = config["token_endpoint"]
        
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
        userinfo_endpoint = config["userinfo_endpoint"]
        userinfo_response = self.get_userinfo_response(userinfo_endpoint)

        return userinfo_response
    

    def authorize(self,request:Request):
        '''
            Authorizes the user through redirecting him to the authorize url
        '''
        authorization_endpoint = self.get_provider_cfg()["authorization_endpoint"]

        url = self.get_request_uri(request,authorization_endpoint)
        return redirect(url)


    def callback(self,request:Request):
        '''
            Returns the email from the user
        '''

        # get authentication code
        auth_code = request.args.get("code")

        config = self.get_provider_cfg()

        # get userinfo
        userinfo_response = self.token_request(request,auth_code,config)

        if userinfo_response.json().get("email_verified"):
            email = userinfo_response.json()["email"]

        return email