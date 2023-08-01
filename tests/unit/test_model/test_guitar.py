
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