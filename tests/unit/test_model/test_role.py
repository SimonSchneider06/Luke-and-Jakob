
def test_role_data_correct(customer_role):
    '''
        `GIVEN` a Role Model
        `WHEN` a new role is created
        `THEN` check if name is stored correctly
    '''

    assert customer_role.name == "Customer"