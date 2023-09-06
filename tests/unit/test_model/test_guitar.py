import pytest
from website import db
from website.models import Guitar
from sqlalchemy import select


def test_guitar_data_correct(new_guitar):
    '''
        `GIVEN` a guitar Model
        `WHEN` a new guitar is created
        `THEN` check if data is stored correctly
    '''

    assert new_guitar.name == "Test"
    assert new_guitar.price == 1500
    assert new_guitar.stock == 5
    assert new_guitar.stripe_price_id == "price_1N4QMpGKMAM99iKsPRgqFrgU"
    assert new_guitar.description == "Die Perfekte Gitarre für Anfänger bis Profi"


def test_check_guitar_exists(test_app):
    '''
        `GIVEN` a guitar method
        `WHEN` a existing guitar gets passed
        `THEN` check if True gets returned
    '''

    with test_app.app_context():

        guitar = db.session.get(Guitar,1)
        assert Guitar.check_guitar_exists(guitar) == True


def test_check_guitar_exists_id_None(new_guitar,test_app):
    '''
        `GIVEN` a guitar method
        `WHEN` a not existing guitar, id = None gets passed
        `THEN` check if False gets returned
    '''

    with test_app.app_context():

        assert Guitar.check_guitar_exists(new_guitar) == False


def test_check_guitar_exists_invalid_type(test_app):
    '''
        `GIVEN` a guitar method
        `WHEN` an argument of invalid type (=string) gets passed
        `THEN` check if TypeError gets raised
    '''

    with test_app.app_context():

        guitar = "Guitar"

        with pytest.raises(TypeError):
            Guitar.check_guitar_exists(guitar)


def test_check_guitar_exists_not_existing(test_app):
    '''
        `GIVEN` a guitar method
        `WHEN` a not existing guitar, gets passed
        `THEN` check if False gets returned
    '''

    with test_app.app_context():

        guitar = Guitar(
            id = 5,
            name = "Test",
            price = 1500,
            stock = 5,
            stripe_price_id = "price_1N4QMpGKMAM99iKsPRgqFrgU",
            description = "Die Perfekte Gitarre für Anfänger bis Profi"
        )

        assert Guitar.check_guitar_exists(guitar) == False


def test_check_guitar_exists_by_name(test_app):
    '''
        `GIVEN` a guitar method
        `WHEN` a guitarname of an existing guitar, gets passed
        `THEN` check if True gets returned
    '''

    with test_app.app_context():

        assert Guitar.check_guitar_exists_by_name("Test") == True


def test_check_guitar_exists_by_name_not_existing(test_app):
    '''
        `GIVEN` a guitar method
        `WHEN` a guitarname of a not existing guitar, gets passed
        `THEN` check if False gets returned
    '''

    with test_app.app_context():

        assert Guitar.check_guitar_exists_by_name("Not_Existing") == False


def test_get_guitar_by_name(test_app,new_guitar):
    '''
        `GIVEN` a guitar method
        `WHEN` a guitarname of a existing guitar, gets passed
        `THEN` check if guitar gets returned
    '''

    with test_app.app_context():

        query = select(Guitar).where(Guitar.name == new_guitar.name)
        guitar = db.session.scalar(query)

        assert Guitar.get_by_name(new_guitar.name) == guitar