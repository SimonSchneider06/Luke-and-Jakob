
def test_home(test_client,home_route):
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/") gets requested
        `THEN` check that response is valid
    '''

    
    response = test_client.get(home_route)

    assert response.status_code == 200
    assert b'Ueberschrift-Fett-Fueller' in response.data
    assert b'Einfacher Text, soll hier nur als Fueller dienen' in response.data
    assert b'Kaufen' in response.data


def test_navbar(test_client,home_route):
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/") gets requested
        `THEN` check that response is valid, test the navbar
    '''

    response = test_client.get(home_route)

    assert response.status_code == 200
    assert b'Shop' in response.data
    assert b'About us' in response.data
    assert b'Login' in response.data


def test_about_us(test_client,about_us_route):
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/about_us") gets requested
        `THEN` check that response is valid
    '''

    response = test_client.get(about_us_route)

    assert response.status_code == 200

    assert b'Ueber uns' in response.data

    # anfang und Ende vom Paragraph
    assert b'In unserer Werkstatt' in response.data
    assert b'gefertigt' in response.data


def test_shopping_cart(test_client,shopping_cart_route):
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/cart") gets requested
        `THEN` check that response is valid
    '''

    response = test_client.get(shopping_cart_route)

    assert response.status_code == 200

    assert b'Ihr Einkaufswagen' in response.data


def test_shop(test_client,shop_route):
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/shop") gets requested
        `THEN` check that response is valid
    '''

    response = test_client.get(shop_route)

    assert response.status_code == 200

    assert b"Unsere Produkte" in response.data


def test_product_site(test_client,product_site_route):
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/product/<product_name>") [product_name = Test] gets requested
        `THEN` check that response is valid
    '''

    response = test_client.get(product_site_route)

    assert response.status_code == 200

    assert b"Test" in response.data
    assert b"In den Einkaufswagen" in response.data


def test_services(test_client,services_route):
    '''
        `GIVEN` a views route
        `WHEN` the Page ("/services") gets requested
        `THEN` check that response is valid
    '''

    response = test_client.get(services_route)

    assert response.status_code == 200

    assert b"Dienstleistungen" in response.data