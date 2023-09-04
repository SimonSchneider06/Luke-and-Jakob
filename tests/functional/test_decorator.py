from flask import Flask
from flask.testing import FlaskClient
from flask_login.test_client import FlaskLoginClient

from website.models import User


def test_decorator_admin_required(test_app:Flask,admin_page_route:str,new_user:User):
    '''
        :param:`GIVEN` a decorator function
        :param:`WHEN` a user, who is logged in, but not an admin tries to request the page
        :param:`THEN` check if 403 error is returned
    '''

    with test_app.test_request_context():
        
        test_app.test_client_class = FlaskLoginClient

        # get user though db, because id is needed
        user = User.get_from_email(new_user.email)

        with test_app.test_client(user = user) as client:
            # user is already logged in because of FlaskLoginClient
            response = client.get(admin_page_route)

            assert response.status_code == 403


def test_decorator_admin_required_passed(test_app:Flask,admin_page_route:str,admin_user:User):
    '''
        :param:`GIVEN` a decorator function
        :param:`WHEN` a logged in user, who is an admin requests the page
        :param:`THEN` check if page is loaded properly
    '''

    with test_app.test_request_context():
        
        test_app.test_client_class = FlaskLoginClient

        # get user though db, because id is needed
        user = User.get_from_email(admin_user.email)

        with test_app.test_client(user = user) as client:
            # user is already logged in because of FlaskLoginClient
            response = client.get(admin_page_route)

            assert response.status_code == 200
            assert b"Admin Page" in response.data