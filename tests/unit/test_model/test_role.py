from website.models import Role
from website import db 
from sqlalchemy import select

def test_role_data_correct(customer_role):
    '''
        `GIVEN` a Role Model
        `WHEN` a new role is created
        `THEN` check if name is stored correctly
    '''

    assert customer_role.name == "Customer"


def test_check_role_exists_by_name(customer_role,test_app):
    '''
        :param:`GIVEN` a Role Method
        :param:`WHEN` a role name of a in the database existing Role gets passed
        :param:`THEN` check if true gets returned 
    '''
    #test_app = create_app("testing")
    with test_app.app_context():
        assert Role.check_role_exists_by_name(customer_role.name) == True


def test_check_role_exists_by_name_not_existing(test_app):
    '''
        :param:`GIVEN` a Role Method
        :param:`WHEN` a role name of a in the database not existing Role gets passed
        :param:`THEN` check if true gets returned 
    '''

    with test_app.app_context():
        assert Role.check_role_exists_by_name("not_existing") == False


def test_get_role_by_name(test_app,customer_role):
    '''
        :param:`GIVEN` a Role Method
        :param:`WHEN` a existing role name  gets passed
        :param:`THEN` check if Role gets returned 
    '''

    with test_app.app_context():
        # get role from db
        query = select(Role).where(Role.name == customer_role.name)
        role = db.session.scalar(query)

        assert Role.get_role_by_name(customer_role.name) == role