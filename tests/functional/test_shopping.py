from flask.testing import FlaskClient
from flask import Flask

from website.models import Guitar
from website.shoppingCart import CartManager

def test_add_to_cart_product_no_session_cart(test_app:Flask,shopping_add_to_cart_route,test_client:FlaskClient,product_site_route,new_guitar):
    '''
        :param:`GIVEN` a shopping route
        :param:`WHEN` an existing product_id gets passed and session_cart doesn't exist
        :param:`THEN` check if flash_message and redirect correct
    '''

    expected_flash_message = b'Produkt erfolgreich im Einkaufswagen'

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = shopping_add_to_cart_route(guitar.id)

    response = test_client.post(route,follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data
    assert response.request.path == product_site_route


def test_add_to_cart_product_session_cart(test_app:Flask,shopping_add_to_cart_route,test_client:FlaskClient,product_site_route,new_guitar):
    '''
        :param:`GIVEN` a shopping route
        :param:`WHEN` an existing product_id gets passed and session_cart exists
        :param:`THEN` check if flash_message and redirect correct
    '''

    expected_flash_message = b'Produkt erfolgreich im Einkaufswagen'

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = shopping_add_to_cart_route(guitar.id)

    # create session["cart"] object
    with test_client.session_transaction() as sess:
        sess["cart"] = [CartManager().create_product_dict(guitar.id,1)]

    # needs to run after the session_transaction block !!
    response = test_client.post(route,follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data
    assert response.request.path == product_site_route


def test_delete_from_cart_product_session_cart(test_app:Flask,shopping_delete_from_cart_route,test_client:FlaskClient,shopping_cart_route,new_guitar):
    '''
        :param:`GIVEN` a shopping route
        :param:`WHEN` an existing product_id gets passed and session_cart exists
        :param:`THEN` check if flash_message and redirect correct
    '''

    expected_flash_message = b'Produkt erfolgreich aus dem Einkaufswagen'

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = shopping_delete_from_cart_route(guitar.id)

    # create session["cart"] object
    with test_client.session_transaction() as sess:
        sess["cart"] = [CartManager().create_product_dict(guitar.id,1)]

    # needs to run after the session_transaction block !!
    response = test_client.get(route,follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data
    assert response.request.path == shopping_cart_route


def test_set_product_quantity_session_cart(test_app:Flask,shopping_set_product_quantity_route,test_client:FlaskClient,shopping_cart_route,new_guitar):
    '''
        :param:`GIVEN` a shopping route
        :param:`WHEN` an existing product_id gets passed and session_cart exists
        :param:`THEN` check if flash_message and redirect correct
    '''

    expected_flash_message = b'Produktmenge erfolgreich'

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = shopping_set_product_quantity_route(id = guitar.id, quantity = 3)

    # create session["cart"] object
    with test_client.session_transaction() as sess:
        sess["cart"] = [CartManager().create_product_dict(guitar.id,1)]

    # needs to run after the session_transaction block !!
    response = test_client.get(route,follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data
    assert response.request.path == shopping_cart_route