import pytest
from flask import Flask

from tests.testSetup import TestDatabaseSetup,TestDataSetup
from website.models import User

def test_database_setup_and_teardown(test_app:Flask,new_user):
    '''
        :param:`GIVEN` the database teardown method
        :param:`WHEN` the app gets passed
        :param:`THEN` check if db gets torn down  
    '''

    TestDatabaseSetup.database_teardown(test_app)

    # calls exception because db not existing anymore
    with pytest.raises(Exception):
        with test_app.app_context():
            user = User.get_from_email(new_user.email)

    # rebuild db again
    test_data = TestDataSetup().create_all_test_data()

    TestDatabaseSetup.database_setup(test_app,test_data)

    # user is back in db
    with test_app.app_context():
        assert User.check_email_exists(new_user.email) == True