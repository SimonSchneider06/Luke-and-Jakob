from flask import Flask
from flask.testing import FlaskClient

import responses
import time
import json
import stripe

from website.models import Guitar
from website.shoppingCart import CartManager


@responses.activate
def test_stripe_checkout(test_app:Flask,stripe_checkout_route,login_test_client:FlaskClient,new_guitar,home_route):
    '''
        :param:`GIVEN` a stripe route
        :param:`WHEN` a logged in user tryes to request it
        :param:`THEN` check if status_code and redirect correct
    '''

    ### url_1 = "https://checkout.stripe.com/v1/checkout/sessions"
    url = "https://api.stripe.com/v1/checkout/sessions"   # this is the api, which gets called

    # got url from
        # https://stripe.com/docs/api/checkout/sessions
        # https://stripe.com/docs/api/checkout/sessions/object#checkout_session_object-url
        # https://stripe.com/docs/api/checkout/sessions/create

    json_data = {"url":home_route}  #only data needed for this test

    with test_app.test_request_context():
        guitar = Guitar.get_by_name(new_guitar.name)

        responses.add(
            responses.POST,
            url = url,
            json = json_data
        )

    # create session["cart"] object
    with login_test_client.session_transaction() as sess:
        sess["cart"] = [CartManager().create_product_dict(guitar.id,1)]

    # needs to run after the session_transaction block !!
    response = login_test_client.post(stripe_checkout_route,follow_redirects = True)

    assert response.status_code == 200
    assert response.request.path == home_route


def test_stripe_webhook_without_header(stripe_webhook_route,login_test_client:FlaskClient):
    '''
        :param:`GIVEN` a stripe route
        :param:`WHEN` the webhook gets called, without header
        :param:`THEN` check if error thrown
    '''

    response = login_test_client.post(stripe_webhook_route)

    assert response.status_code == 400


def test_stripe_webhook(test_app:Flask,stripe_webhook_route,login_test_client:FlaskClient):
    '''
        :param:`GIVEN` a stripe route
        :param:`WHEN` the webhook gets called
        :param:`THEN` check if 200 gets returned
    '''

    # only data needed for test
    evt_data = {
                "id":"evt_123",
                "type":"checkout.session.completed",
                "data":{"object":{"client_reference_id":1}}
                }
    
    data = json.dumps(evt_data)


    with test_app.app_context():
        #signed_header = generate_signature_header(json.dumps(evt_data),secret = test_app.config["PAYMENT_SERVICES"]["stripe"]["endpoint_key"])
        header = generate_header(payload = data,secret = test_app.config["PAYMENT_SERVICES"]["stripe"]["endpoint_key"])

    response = login_test_client.post(stripe_webhook_route,data = data,headers = {"Stripe-Signature":header})

    assert response.status_code == 200


#https://github.com/stripe/stripe-python/blob/master/tests/test_webhook.py

DUMMY_WEBHOOK_SECRET = "whsec_test_secret"

DUMMY_WEBHOOK_PAYLOAD = """{"id": "evt_test_webhook","object": "event"}"""

def generate_header(**kwargs):
    timestamp = kwargs.get("timestamp", int(time.time()))
    payload = kwargs.get("payload", DUMMY_WEBHOOK_PAYLOAD)
    secret = kwargs.get("secret", DUMMY_WEBHOOK_SECRET)
    scheme = kwargs.get("scheme", stripe.WebhookSignature.EXPECTED_SCHEME)
    signature = kwargs.get("signature", None)
    if signature is None:
        payload_to_sign = "%d.%s" % (timestamp, payload)
        signature = stripe.WebhookSignature._compute_signature(
            payload_to_sign, secret
        )
    header = "t=%d,%s=%s" % (timestamp, scheme, signature)
    return header