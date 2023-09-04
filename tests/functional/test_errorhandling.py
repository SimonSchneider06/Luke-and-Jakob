from flask import Flask
from flask.testing import FlaskClient


def test_page_not_found_error(test_app:Flask):
    '''
        `GIVEN` a errorhandling function
        `WHEN` the 404 error gets raised(url which doesn't exist gets called)
        `THEN` check that errorpage gets shown
    '''

    
    with test_app.test_client() as test_client:
        response = test_client.get("/test_404_error")

        assert response.status_code == 404

        assert b"Die gesuchte Seite ist nicht auffindbar." in response.data
        assert b'Das ist alles was wir wissen.' in response.data


def test_internal_server_error():
    '''
        `GIVEN` a errorhandling function
        `WHEN` the 500 error gets raised, internal server error
        `THEN` check that errorpage gets shown
    '''

    # don't know how to test, tryed it with debug mode off and an error in flask template 
    # --> redirected one to the errorpage and had thrown a 500 response status code
    # Problem ist, dass jeder Serverfehler hier als Exception ausgeworfen wird und dadurch
    # kein 500 status code zustande kommt. 
    pass

def test_page_forbidden_error(test_client:FlaskClient,admin_page_route:str):
    '''
        `GIVEN` a errorhandling function
        `WHEN` the 403 error gets raised, page forbidden for user
        `THEN` check that errorpage gets shown
    '''
    
    response = test_client.get(admin_page_route)

    assert response.status_code == 403

    assert b"Die gesuchte Seite ist nicht auffindbar." in response.data
    assert b'Das ist alles was wir wissen.' in response.data