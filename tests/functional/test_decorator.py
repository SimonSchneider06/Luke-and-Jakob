from flask.testing import FlaskClient


def test_decorator_admin_required(admin_page_route:str,login_test_client:FlaskClient):
    '''
        :param:`GIVEN` a decorator function
        :param:`WHEN` a user, who is logged in, but not an admin tries to request the page
        :param:`THEN` check if 403 error is returned
    '''

    # user is already logged in because of login_test_client
    response = login_test_client.get(admin_page_route)

    assert response.status_code == 403


def test_decorator_admin_required_passed(admin_page_route:str,login_admin_test_client:FlaskClient):
    '''
        :param:`GIVEN` a decorator function
        :param:`WHEN` a logged in user, who is an admin requests the page
        :param:`THEN` check if page is loaded properly
    '''

    # user is already logged in because of login_admin_test_client
    response = login_admin_test_client.get(admin_page_route)

    assert response.status_code == 200
    assert b"Admin Page" in response.data