from website import create_app

def test_home():
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/") gets requested
        `THEN` check that response is valid
    '''

    test_app = create_app("testing")
    
    with test_app.test_client() as test_client:
        response = test_client.get("/")

        assert response.status_code == 200
        assert b'Ueberschrift-Fett-Fueller' in response.data
        assert b'Einfacher Text, soll hier nur als Fueller dienen' in response.data
        assert b'Kaufen' in response.data


def test_navbar():
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/") gets requested
        `THEN` check that response is valid, test the navbar
    '''

    test_app = create_app("testing")
    
    with test_app.test_client() as test_client:
        response = test_client.get("/")

        assert response.status_code == 200
        assert b'Shop' in response.data
        assert b'About us' in response.data
        assert b'Login' in response.data


def test_about_us():
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/about_us") gets requested
        `THEN` check that response is valid
    '''

    test_app = create_app("testing")
    
    with test_app.test_client() as test_client:
        response = test_client.get("/about_us")

        assert response.status_code == 200

        assert b'Ueber uns' in response.data

        # anfang und Ende vom Paragraph
        assert b'In unserer Werkstatt' in response.data
        assert b'gefertigt' in response.data

def test_shopping_cart():
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/cart") gets requested
        `THEN` check that response is valid
    '''

    test_app = create_app("testing")
    
    with test_app.test_client() as test_client:
        response = test_client.get("/cart")

        assert response.status_code == 200

        assert b'Ihr Einkaufswagen' in response.data


def test_shop():
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/shop") gets requested
        `THEN` check that response is valid
    '''

    test_app = create_app("testing")
    
    with test_app.test_client() as test_client:
        response = test_client.get("/shop")

        assert response.status_code == 200

        assert b"Unsere Produkte" in response.data


def test_product_site():
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/product/<product_name>") [product_name = Test] gets requested
        `THEN` check that response is valid
    '''

    test_app = create_app("testing")
    
    with test_app.test_client() as test_client:
        response = test_client.get("/product/Test")

        assert response.status_code == 200

        assert b"Test" in response.data
        assert b"In den Einkaufswagen" in response.data


def test_services():
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/services") gets requested
        `THEN` check that response is valid
    '''

    test_app = create_app("testing")
    
    with test_app.test_client() as test_client:
        response = test_client.get("/services")

        assert response.status_code == 200

        assert b"Dienstleistungen" in response.data