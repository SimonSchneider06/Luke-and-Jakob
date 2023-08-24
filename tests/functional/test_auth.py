from website import create_app

def test_logout():
    '''
        `GIVEN` a auth route
        `WHEN` a not logged in user requests /logout
        `THEN` check if error get`s raised
    '''

    test_app = create_app("testing")
    with test_app.app_context():
        with test_app.test_client() as test_client:
            response = test_client.get("/logout")

            assert response.status_code == 302


def test_sign_up():
    '''
        `GIVEN` a auth route
    '''