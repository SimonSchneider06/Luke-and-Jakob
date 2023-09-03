import pytest
from flask import Flask,url_for

from website.models import User,Role,Guitar 
from tests.testClient import CustomClient
from tests.testSetup import TestDatabaseSetup,TestDataSetup,TestAppSetup, RouteSetup


def pytest_configure(config):
    '''
        Run before the tests to configure the testing environment
    '''

    testApp = TestAppSetup.create_test_app()
    testData = TestDataSetup().create_all_test_data()

    TestDatabaseSetup.database_setup(testApp,testData)

    print("SETUP SUCCESSFUL")


def pytest_sessionfinish(session,exitstatus):
    '''
        Called after all Tests
        Teardown TestDatabase
    '''
    # https://docs.pytest.org/en/latest/reference/reference.html#pytest.hookspec.pytest_sessionfinish
    # https://docs.pytest.org/en/latest/reference/reference.html#exitcode

    testApp = TestAppSetup.create_test_app()

    TestDatabaseSetup.database_teardown(testApp)

    # first character doesn't get shown
    print("TEARDOWN SUCCESSFUL")


@pytest.fixture(scope = "module")
def admin_role() -> Role:
    '''
        Returns the admin role
    '''
    role = TestDataSetup().create_admin_role()
    return role


@pytest.fixture()
def test_app():
    '''
        Returns a testapp
    '''
    test_app = TestAppSetup.create_test_app()

    yield test_app


@pytest.fixture()
def test_client(test_app:Flask,role:str = "Customer"):
    '''
        Returns a test_client with authorisation
        :param: `authorisation` is a string with default value of `Customer`
    '''
    test_app.test_client_class = CustomClient
    return test_app.test_client(role = role)


@pytest.fixture(scope = "module")
def customer_role() -> Role:
    '''
        Returns the customer role
    '''
    role = TestDataSetup().create_customer_role()
    return role


@pytest.fixture(scope = "module")
def new_user(customer_role:Role) -> User:
    '''
        Create a new, valid user
    '''
    user = TestDataSetup().create_user(customer_role)
        
    return user


@pytest.fixture(scope = "module")
def third_party_user(customer_role:Role) -> User:
    '''
        Create a valid third party user
    '''
    user = TestDataSetup().create_third_party_user(customer_role)

    return user


@pytest.fixture(scope = "function")
def shopping_order() -> list[dict]:
    '''
        Create a shopping order
    '''

    order = [{"id":1,"quantity":1}]

    return order


@pytest.fixture(scope = "module")
def new_guitar() -> Guitar:
    '''
        Create a new Guitar
    '''
    guitar = TestDataSetup().create_guitar()

    return guitar


@pytest.fixture()
def log_user_in(new_user,test_client,login_route,home_route) -> None:
    '''
        Logs the new_user in 
    '''

    # make test response to home route
    # test_response = test_client.get(home_route)
    # check if login in navbar. if it is, client isn't logged in
    # if b'Login' in test_response.data:

    test_client.post(login_route,data = {
        "email": new_user.email,
        "password": "Save_Password4"
    },follow_redirects = True)


@pytest.fixture()
def log_user_out(test_client,logout_route,home_route) -> None:
    '''
        Logs a currently logged in user out
    '''

    # check if currently logged in
    test_response = test_client.get(home_route)
    # check if login in navbar. If it is client isn't logged in
    if b'Login' not in test_response.data:
        test_client.get(logout_route,follow_redirects = True)


# routes----------

# auth routes---------
@pytest.fixture()
def sign_up_route(test_app) -> str:
    '''
        Returns the sign_up route
    '''
    return RouteSetup.get_route_by_name(test_app,"auth.sign_up")


@pytest.fixture()
def login_route(test_app) -> str:
    '''
        Returns the login route
    '''
    return RouteSetup.get_route_by_name(test_app,"auth.login")


@pytest.fixture()
def logout_route(test_app) -> str:
    '''
        Returns the logout route
    '''
    return RouteSetup.get_route_by_name(test_app,"auth.logout")


@pytest.fixture()
def change_user_data_route(test_app) -> str:
    '''
        Returns the change_user_data route
    '''
    return RouteSetup.get_route_by_name(test_app,"auth.change_user_data")


@pytest.fixture()
def account_page_route(test_app) -> str:
    '''
        Returns the account_page route
    '''
    return RouteSetup.get_route_by_name(test_app,"auth.account_page")


@pytest.fixture()
def password_reset_route(test_app) -> str:
    '''
        Returns the password_reset route
    '''
    return RouteSetup.get_route_by_name(test_app,"auth.password_reset")


@pytest.fixture()
def new_password_route(test_app) -> str:
    '''
        Returns the new_password route
    '''

    def _get_route_by_token(token):
        #print(token)
        route =  RouteSetup.get_route_by_name(test_app,f"auth.new_password",token = token)
        #print(route)

        return route

    return _get_route_by_token

# views routes--------
@pytest.fixture()
def home_route(test_app) -> str:
    '''
        Returns the home route
    '''
    return RouteSetup.get_route_by_name(test_app,"views.home")


@pytest.fixture()
def about_us_route(test_app) -> str:
    '''
        Returns the about_us route
    '''
    return RouteSetup.get_route_by_name(test_app,"views.about_us")


@pytest.fixture()
def services_route(test_app) -> str:
    '''
        Returns the services route
    '''
    return RouteSetup.get_route_by_name(test_app,"views.services")


@pytest.fixture()
def shopping_cart_route(test_app) -> str:
    '''
        Returns the shopping_cart route
    '''
    return RouteSetup.get_route_by_name(test_app,"views.shopping_cart")


@pytest.fixture()
def shop_route(test_app) -> str:
    '''
        Returns the shop route
    '''
    return RouteSetup.get_route_by_name(test_app,"views.shop")


@pytest.fixture()
def product_site_route(test_app,new_guitar) -> str:
    '''
        Returns the product_site route, for the test Product in the database
    '''

    product_name = new_guitar.name

    return RouteSetup.get_route_by_name(test_app,"views.product_site",product_name = product_name)