from website.shoppingCart import StripeCartConverter
from website import create_app

from website.shoppingCart import CartManager    # for creating dicts to test better
                                                # line 25

def test_StripeCartConverter_convert_dict():
    '''
        `GIVEN` a StripeCartConverter model
        `WHEN` a product id and quantity are given
        `THEN` check if new stripe dict, for checkout gets created
    '''

    test_app = create_app("testing")
    with test_app.app_context():
        assert StripeCartConverter().convert_dict(1,1) == {"price":"price_1N4QMpGKMAM99iKsPRgqFrgU","quantity":1}

def test_StripeCartConverter_convert_all_dicts(shopping_order):
    '''
        `GIVEN` a StripeCartConverter model
        `WHEN` the entire shopping cart should be converted
        `THEN` check if converted correctly
    '''

    # make a bigger shopping order
    test_dict_2 = CartManager().create_product_dict(1,3)
    shopping_order.append(test_dict_2)

    test_app = create_app("testing")
    with test_app.app_context():
        assert StripeCartConverter().convert_all_dicts(shopping_order) == [{"price":"price_1N4QMpGKMAM99iKsPRgqFrgU","quantity":1},{"price":"price_1N4QMpGKMAM99iKsPRgqFrgU","quantity":3}]


def test_StripeCartConverter_convert_all_dicts_empty_cart():
    '''
        `GIVEN` a StripeCartConverter model
        `WHEN` an empty cart gets passed as argument
        `THEN` check if None gets returned
    '''

    none_variable = None

    test_app = create_app("testing")
    with test_app.app_context():
        assert StripeCartConverter().convert_all_dicts([]) == None
        assert StripeCartConverter().convert_all_dicts(none_variable) == None