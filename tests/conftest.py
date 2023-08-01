import pytest

from website.models import User,Role,Guitar 

@pytest.fixture(scope = "module")
def customer_role() -> Role:
    '''
        Returns the customer role
    '''
    role = Role(name = "Customer")
    return role


@pytest.fixture(scope = "module")
def new_user(customer_role:callable) -> User:
    '''
        Create a new, valid user
    '''
    user = User(
        email = "schneider_berghausen@web.de",
        firstName = "Simon",
        lastName = "Schneider",
        street = "Zum Wacholdertal",
        houseNumber = "1",
        plz = "93336",
        city = "Altmannstein",
        country = "Deutschland",
        password = "Save_Password",
        rememberMe = True,
        thirdParty = False,
        role = customer_role
    )
        
    return user

@pytest.fixture(scope = "module")
def shopping_order() -> list:
    '''
        Create a shopping order
    '''

    order = [{"id":1,"quantity":1},{"id":2,"quantity":1}]

    return order

@pytest.fixture(scope = "module")
def new_guitar() -> Guitar:
    '''
        Create a new Guitar
    '''
    guitar = Guitar(
        name = "Test",
        price = 1500,
        stock = 5,
        stripe_price_id = "price_1N4QMpGKMAM99iKsPRgqFrgU",
        description = "Die Perfekte Gitarre für Anfänger bis Profi"
    )

    return guitar