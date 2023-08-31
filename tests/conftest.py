import pytest
from flask import Flask

from website.models import User,Role,Guitar 
from tests.testClient import CustomClient
from tests.testSetup import TestDatabaseSetup,TestDataSetup,TestAppSetup


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
def new_user(customer_role:callable) -> User:
    '''
        Create a new, valid user
    '''
    user = TestDataSetup().create_user(customer_role)
        
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

