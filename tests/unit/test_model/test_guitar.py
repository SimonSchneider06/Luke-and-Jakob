import pytest
from website import db,create_app
from sqlalchemy import select
from website.models import Guitar


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


def test_check_guitar_exists():
    '''
        `GIVEN` a guitar method
        `WHEN` a existing guitar gets passed
        `THEN` check if True gets returned
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        guitar = db.session.get(Guitar,1)
        assert Guitar.check_guitar_exists(guitar) == True


def test_check_guitar_exists_id_None(new_guitar):
    '''
        `GIVEN` a guitar method
        `WHEN` a not existing guitar, id = None gets passed
        `THEN` check if False gets returned
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        assert Guitar.check_guitar_exists(new_guitar) == False


def test_check_guitar_exists_invalid_type():
    '''
        `GIVEN` a guitar method
        `WHEN` an argument of invalid type (=string) gets passed
        `THEN` check if TypeError gets raised
    '''

    test_app = create_app("testing")
    with test_app.app_context():

        guitar = "Guitar"

        with pytest.raises(TypeError):
            Guitar.check_guitar_exists(guitar)


def test_check_guitar_exists_not_existing():
    '''
        `GIVEN` a guitar method
        `WHEN` a not existing guitar, gets passed
        `THEN` check if False gets returned
    '''

    test_app = create_app("testing")
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