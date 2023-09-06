from flask import Flask
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from contextlib import ExitStack
import os

from website import db
from website.models import Guitar
from website.ImageManager import ImageManager

from tests.testHelperFn import image_path_setup

def test_add_product_without_images(login_admin_test_client:FlaskClient,admin_add_product_route,test_app:Flask):
    '''
        :param:`GIVEN` a admin route
        :param:`WHEN` an admin tryes to add a new product, without images
        :param:`THEN` check if status code, flash message, redirect correct
    '''

    expected_flash_message = b"Bitte setzen sie Bilder ein"

    new_guitar_name = "Test_Product_Added"

    response = login_admin_test_client.post(admin_add_product_route,data = {
        "product-name":new_guitar_name,
        "price":"2000",
        "stock":"3",
        "description":"A Test Guitar",
        "stripe_price_id":"Not_existing_one"
    },follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data
    assert response.request.path == admin_add_product_route

    # check that guitar didn't got added
    with test_app.app_context():
        assert Guitar.check_guitar_exists_by_name(new_guitar_name) == False


def test_add_product_name_exists_already(login_admin_test_client:FlaskClient,admin_add_product_route,new_guitar):
    '''
        :param:`GIVEN` a admin route
        :param:`WHEN` an admin tryes to add a new product, but name exists already
        :param:`THEN` check if status code, flash message, redirect correct
    '''

    expected_flash_message = b"Gitarren Name existiert schon"

    # passes a file, so front_img check doesn't get called
    with open("./tests/test_files/test_img.png","rb") as f:
        file = FileStorage(f)

        response = login_admin_test_client.post(admin_add_product_route,data = {
            "product-name":new_guitar.name,
            "price":"2000",
            "stock":"3",
            "description":"A Test Guitar",
            "stripe_price_id":"Not_existing_one",
            "image-deck":file
        },follow_redirects = True)

        assert response.status_code == 200
        assert expected_flash_message in response.data
        assert response.request.path == admin_add_product_route


def test_add_product_name_empty_field(login_admin_test_client:FlaskClient,admin_add_product_route:str):
    '''
        :param:`GIVEN` a admin route
        :param:`WHEN` an admin tryes to add a new product, but name exists already
        :param:`THEN` check if status code, flash message, redirect correct
    '''

    expected_flash_message = b"sie alle Felder aus"

    # passes a file, so front_img check doesn't get called
    with open("./tests/test_files/test_img.png","rb") as f:
        file = FileStorage(f)

        response = login_admin_test_client.post(admin_add_product_route,data = {
            "product-name":"Also_Not_existing",
            "price":"2000",
            "stock":"3",
            "description":"A Test Guitar",
            "stripe_price_id":"",
            "image-deck":file
        },follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data
    assert response.request.path == admin_add_product_route


def test_add_product_name_invalid_files(login_admin_test_client:FlaskClient,admin_add_product_route,new_guitar):
    '''
        :param:`GIVEN` a admin route
        :param:`WHEN` an admin tryes to add a new product, but name exists already
        :param:`THEN` check if status code, flash message, redirect correct
    '''

    expected_flash_message = b"oder nicht vorhanden, bitte versuchen Sie es erneut"

    # passes a file, so front_img check doesn't get called
    with open("./tests/test_files/test_img.png","rb") as f:
        file = FileStorage(f)

        with open("./tests/test_files/test_pdf.pdf","rb") as pdf_data:
            pdf = FileStorage(pdf_data)

            response = login_admin_test_client.post(admin_add_product_route,data = {
                "product-name":"Not_Existing",
                "price":"2000",
                "stock":"3",
                "description":"A Test Guitar",
                "stripe_price_id":"Not_existing_one",
                "image-deck":file,
                "image": [pdf]
            },follow_redirects = True)

        assert response.status_code == 200
        assert expected_flash_message in response.data
        assert response.request.path == admin_add_product_route


def test_add_product_name_valid(login_admin_test_client:FlaskClient,admin_add_product_route,test_app:Flask,admin_page_route):
    '''
        :param:`GIVEN` a admin route
        :param:`WHEN` an admin tryes to add a new product, but name exists already
        :param:`THEN` check if status code, flash message, redirect correct
    '''

    expected_flash_message = b"Erfolgreich neues Modell"

    product_name = "New Model VX"

    # get extensions of files and folder path
    ext_list = ["0.png","1.JPG","2.JPG","3.png","4.JPG"]
    folder_path = "./tests/test_files/img_of_Test_model"

    result = image_path_setup(ext_list,folder_path)

    filenames_without_front_img = result[0]
    front_img_path = result[1]

    # passes a file, so front_img check doesn't get called
    with ExitStack() as stack:
        file_list = [stack.enter_context(open(fname,"rb")) for fname in filenames_without_front_img]
        file = stack.enter_context(open(front_img_path,"rb"))

        file = FileStorage(file)
        img_list = []
        for item in file_list:
            item_F = FileStorage(item)
            img_list.append(item_F)

        response = login_admin_test_client.post(admin_add_product_route,data = {
            "product-name":product_name,
            "price":"2000",
            "stock":"3",
            "description":"A New Guitar Model",
            "stripe_price_id":"Not_existing_one",
            "image-deck":file,
            "image": img_list
        },follow_redirects = True)

        assert response.status_code == 200
        assert expected_flash_message in response.data
        assert response.request.path == admin_page_route

    # check that product exists
    with test_app.app_context():
        assert Guitar.check_guitar_exists_by_name(product_name) == True
    
        uploaded_path = f'{test_app.config["UPLOAD_PATH"]}/{product_name}'
        # check that images got added
        assert os.path.exists(uploaded_path) == True

        ImageManager().delete_directory_by_product_name(product_name)

        added_guitar = Guitar.get_by_name(product_name)

        db.session.delete(added_guitar)
        db.session.commit()
        # check that deleted
        assert Guitar.check_guitar_exists_by_name(product_name) == False
    