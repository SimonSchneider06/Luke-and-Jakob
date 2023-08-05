from website.shoppingCart import CartManager
import pytest
from website import create_app

def test_CartManager_add_product_empty_cart():
    '''
        `GIVEN` CartManager model and a empty shopping cart and NoneType
        `WHEN` a new product gets added to shopping cart
        `THEN` check if added correcty
    '''

    assert CartManager().add_product(1,[]) == [{"id":1,"quantity":1}]
    assert CartManager().add_product(1,None) == [{"id":1,"quantity":1}]


def test_CartManager_add_new_product_to_existing_cart(shopping_order):
    '''
        `GIVEN` CartManager model and existing shopping cart with valid data
        `WHEN` a new product gets added
        `THEN` check if added correctly
    '''

    assert CartManager().add_product(2,shopping_order) == [{"id":1,"quantity":1},{"id":2,"quantity":1}]

def test_CartManager_add_existing_product_to_existing_cart(shopping_order):
    '''
        `GIVEN` CartManager model and existing shopping cart with valid data
        `WHEN` a product which is already in the shopping cart gets added
        `THEN` check if quantity of that product gets increased by 1 
    '''

    assert CartManager().add_product(1,shopping_order) == [{"id":1,"quantity":2}]


def test_CartManager_check_product_in_order(shopping_order):
    '''
        `GIVEN` a CartManager model and exisiting shopping cart with valid data
        `WHEN` a product, which is already in the cart, and one which isn't 
        `THEN` check that true or false gets returned
    '''

    assert CartManager().check_product_in_order(1,shopping_order) == True
    assert CartManager().check_product_in_order(2,shopping_order) == False


def test_CartManager_set_quantity(shopping_order):
    '''
        `GIVEN` a CartManager model and existing shopping cart with valid data
        `WHEN` the quantity of a product,which is already in the cart, gets set to a value > 0
        `THEN` check if set correctly
    '''

    assert CartManager().set_quantity(1,shopping_order,3) == [{"id":1,"quantity":3}]


def test_CartManager_set_quantity_to_zero(shopping_order):
    '''
        `GIVEN` a CartManager model and existing shopping cart with valid data
        `WHEN` the quantity of a product,which is already in the cart, gets set to 0
        `THEN` check if product gets deleted
    '''
    assert CartManager().set_quantity(1,shopping_order,0) == []

def test_CartManager_set_quantity_of_product_not_in_cart(shopping_order):
    '''
        `GIVEN` a CartManager model and shopping cart with valid data
        `WHEN` the quantity of a product, which is not in the cart, gets set to a value > 0
        `THEN` check if product with that quantity gets added
    '''
    assert CartManager().set_quantity(2,shopping_order,4) == [{"id":1,"quantity":1},{"id":2,"quantity":4}]


def test_CartManager_create_product_dict():
    '''
        `GIVEN` a CartManager model and a product id and quantity
        `WHEN` a dictionary should be created
        `THEN` check if created correcty
    '''
    assert CartManager().create_product_dict(1,1) == {"id":1,"quantity":1}


def test_CartManager_increase_quantity_by_product_in_order(shopping_order):
    '''
        `GIVEN` a CartManager model and shopping cart with valid data
        `WHEN` the quantity of a product should be increased
        `THEN` check if increased by 1
    '''
    assert CartManager().increase_quantity(1,shopping_order) == [{"id":1,"quantity":2}]


def test_CartManager_increase_quantity_by_product_not_in_order(shopping_order):
    '''
        `GIVEN` a CartManager model and shopping cart with valid data
        `WHEN` the quantity of a product, not in cart should be increased
        `THEN` check if ValueError gets raised
    '''
    with pytest.raises(ValueError):
        CartManager().increase_quantity(2,shopping_order)


def test_CartManager_delete_product_by_product_in_order(shopping_order):
    '''
        `GIVEN` a CartManager model and a shopping order, with valid data
        `WHEN` a product, in the cart gets deleted
        `THEN` check if deleted correctly
    '''
    assert CartManager().delete_product(1,shopping_order) == []

    # make shopping order bigger to test, when multiple dicts in it
    shopping_order = CartManager().add_product(1,shopping_order)
    shopping_order = CartManager().add_product(2,shopping_order)

    assert CartManager().delete_product(1,shopping_order) == [{"id":2,"quantity":1}]


def test_CartManager_delete_product_by_product_not_in_order(shopping_order):
    '''
        `GIVEN` a CartManager model and a shopping order, with valid data
        `WHEN` a product,not in the cart, trying to delete
        `THEN` check if cart unchanged
    '''

    assert CartManager().delete_product(2,shopping_order) == [{"id":1,"quantity":1}]


def test_CartManager_calculate_total_cart_price(shopping_order):
    '''
        `GIVEN` a CartManager model and a shopping order, with valid data
        `WHEN` a the total price of the shopping cart should be calculated
        `THEN` check if calculated correctly
    '''
    test_app = create_app("testing")
    with test_app.app_context():
        assert CartManager().calculate_total_cart_price(shopping_order) == 1500



def test_CartManager_calculate_total_cart_price_empty_cart():
    '''
        `GIVEN` a CartManager model and an empty cart
        `WHEN` the total price gets calculated
        `THEN` check if returns correctly and doesn't throw error
    '''
    assert CartManager().calculate_total_cart_price([]) == 0

