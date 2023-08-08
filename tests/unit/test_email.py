from website.email import send_email,send_customer_order_email,send_password_reset_email
from website import create_app,mail,db
import pytest
from website.models import User

def test_send_email():
    '''
        `GIVEN` a function to send emails
        `WHEN` valid parameters, a recipient, topic, template gets passed
        `THEN` check if email got send
    '''

    # emails are only send if 'TESTING=False', thats why different class
    test_app = create_app("mail-testing")   

    with test_app.app_context():

        with mail.record_messages() as outbox:
            send_email("schneider_berghausen@web.de","Test-Mail-Sending","test")

            assert len(outbox) == 1
            assert outbox[0].subject == "LUKE&JAKOB Test-Mail-Sending"


def test_send_email_template_not_existing():
    '''
        `GIVEN` a function to send emails
        `WHEN` valid parameters, a recipient, topic,but template doesn't 
        exist gets passed
        `THEN` check that ValueError gets raised and email didn't get sent
    '''

        # emails are only send if 'TESTING=False', thats why different class
    test_app = create_app("mail-testing")   

    with test_app.app_context():

        with mail.record_messages() as outbox:
            with pytest.raises(ValueError):
                send_email("schneider_berghausen@web.de","Test-Mail-Sending","not_existing")

            assert len(outbox) == 0


def test_send_password_reset_email():
    '''
        `GIVEN` a function to send password reset emails
        `WHEN` a valid user gets passed
        `THEN` check that email got send correctly
    '''

    # emails are only send if 'TESTING=False', thats why different class
    test_app = create_app("mail-testing")   

    # needed because of url_for in the template
    with test_app.test_request_context():

        user = db.session.get(User,1)

        with mail.record_messages() as outbox:
            
            send_password_reset_email(user)

            assert len(outbox) == 1
            assert outbox[0].subject == "LUKE&JAKOB Password Reset"


def test_send_password_reset_email_invalid_type():
    '''
        `GIVEN` a function to send password reset emails
        `WHEN` a variable of invalid type gets passed
        `THEN` check that TypeError got raised
    '''

    # emails are only send if 'TESTING=False', thats why different class
    test_app = create_app("mail-testing")   

    invalid_type = "Test"

    # needed because of url_for in the template
    with test_app.app_context():
            
        with pytest.raises(TypeError):
            send_password_reset_email(invalid_type)


def test_send_customer_order_email(shopping_order):
    '''
        `GIVEN` a function to send customer order emails
        `WHEN` a valid user gets passed
        `THEN` check that email got send correctly
    '''

    # emails are only send if 'TESTING=False', thats why different class
    test_app = create_app("mail-testing")   

    # needed because of url_for in the template
    with test_app.test_request_context():

        user = db.session.get(User,1)
        user.set_order(shopping_order)

        with mail.record_messages() as outbox:
            
            send_customer_order_email(user)

            assert len(outbox) == 1
            assert outbox[0].subject == "LUKE&JAKOB Neue Bestellung"
