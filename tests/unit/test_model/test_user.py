import pytest

def test_new_user_data_correct(new_user,customer_role):
    '''
        `GIVEN` a User Model
        `WHEN` a new User is created
        `THEN` check the fields email, firstName, lastName, street,
        houseNumber, plz, city, country, password_hash, rememberMe, date_added,
        thirdParty, order, role_id are defined correctly
    '''

    assert new_user.email == "schneider_berghausen@web.de"
    assert new_user.firstName == "Simon"
    assert new_user.lastName == "Schneider"
    assert new_user.street == "Zum Wacholdertal"
    assert new_user.houseNumber == "1"
    assert new_user.plz == "93336"
    assert new_user.city == "Altmannstein"
    assert new_user.country == "Deutschland"
    assert new_user.verifyPassword("Save_Password") == True
    assert new_user.rememberMe == True
    assert new_user.thirdParty == False
    assert new_user.role_id == customer_role.id


def test_user_store_order(new_user,shopping_order):
    '''
        `GIVEN` a User Model
        `WHEN` a User buys something the order is stored in the database
        `THEN` check if stored correctly
    '''

    new_user.set_order(shopping_order)
    assert new_user.get_order() == shopping_order


def test_user_read_password(new_user):
    '''
        `GIVEN` a User Password
        `WHEN` a someone wants to read it
        `THEN` check if attributeError gets raised
    '''

    with pytest.raises(AttributeError):
        new_user.password