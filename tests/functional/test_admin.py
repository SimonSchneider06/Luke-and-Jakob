from flask import Flask
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from contextlib import ExitStack
import os

from website import db
from website.models import Guitar
from website.ImageManager import ImageManager

from tests.testHelperFn import image_path_setup,recreate_image_in_folder
from tests.testSetup import TestDataSetup

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


def test_add_product_name_invalid_files(login_admin_test_client:FlaskClient,admin_add_product_route):
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


def test_add_product_int_not_valid(login_admin_test_client:FlaskClient,admin_add_product_route):
    '''
        :param:`GIVEN` a admin route
        :param:`WHEN` an admin tryes to add a new product, but name exists already
        :param:`THEN` check if status code, flash message, redirect correct
    '''

    expected_flash_message = b"Geben Sie bei Preis und Anzahl nur Zahlen ein"

    # passes a file, so front_img check doesn't get called
    with open("./tests/test_files/test_img.png","rb") as f:
        file = FileStorage(f)

        response = login_admin_test_client.post(admin_add_product_route,data = {
            "product-name":"Also_Not_existing",
            "price":"2000A",
            "stock":"3",
            "description":"A Test Guitar",
            "stripe_price_id":"Not_existing",
            "image-deck":file
        },follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data


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


def test_change_product_not_existing(login_admin_test_client:FlaskClient,admin_change_product_route):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` this route gets requested, but product doesn't exist
        :param:`THEN` check if 404 error returned
    '''

    not_existing_id = 3293

    route = admin_change_product_route(not_existing_id)

    response = login_admin_test_client.get(route, follow_redirects = True)

    assert response.status_code == 404
    assert b"Die gesuchte Seite ist nicht auffindbar." in response.data
    assert b'Das ist alles was wir wissen.' in response.data


def test_change_product_guitar_name_exists_already(test_app:Flask,login_admin_test_client:FlaskClient,admin_change_product_route,new_guitar):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` valid data gets posted to this route, but the guitarname is already given
        :param:`THEN` check if flash_message correct
    '''

    test_guitar_name = "New Model V2"
    expected_flash_message = b"Gitarre mit diesem Namen existiert schon"

    # create guitar for testing purpose, 2nd in db is needed
    test_guitar = Guitar(
        name = test_guitar_name,
        price = 3000,
        stock = 2,
        stripe_price_id = "not_existing",
        description = "Also has bluetooth"
    )

    with test_app.app_context():

        # add test_guitar to db
        db.session.add(test_guitar)
        db.session.commit()

        guitar = Guitar.get_by_name(new_guitar.name)

    route = admin_change_product_route(guitar.id)

    response = login_admin_test_client.post(route,data = {
        "product-name":test_guitar_name,
        "price":new_guitar.price,
        "stock":new_guitar.stock,
        "description":new_guitar.description,
        "stripe_price_id":new_guitar.stripe_price_id
    }, follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data

    # delete test_guitar from db
    with test_app.app_context():
        db.session.delete(test_guitar)
        db.session.commit()

        assert Guitar.check_guitar_exists_by_name(test_guitar_name) == False


def test_change_product_change_name(test_app:Flask,login_admin_test_client:FlaskClient,admin_change_product_route,new_guitar:Guitar):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` valid data gets posted to this route
        :param:`THEN` check if flash_message correct and product name got changed correct
    '''

    expected_flash_message = b"Product Daten erfolgreich"
    new_name = "Neuer Name"

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = admin_change_product_route(guitar.id)

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

        response = login_admin_test_client.post(route,data = {
            "product-name":new_name,
            "price":f'{new_guitar.price}',
            "stock":f'{new_guitar.stock}',
            "description":new_guitar.description,
            "stripe_price_id":new_guitar.stripe_price_id,
            "img-0":file,
            "img-1":file_list[0],
            "img-2":file_list[1],
            "img-3":file_list[2],
            "img-4":file_list[3]
        }, follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data

    # check name got changed and rename back from db
    with test_app.app_context():
        assert Guitar.check_guitar_exists_by_name(new_name) == True

        guitar = Guitar.get_by_name(new_name)
        # change name back
        guitar.name = new_guitar.name

        db.session.commit()

        assert Guitar.check_guitar_exists_by_name(new_guitar.name) == True


def test_change_product_str_not_valid(test_app:Flask,login_admin_test_client:FlaskClient,admin_change_product_route,new_guitar):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` input data not string
        :param:`THEN` check if flash_message correct
    '''

    expected_flash_message = b"Eingegebene Daten sind nicht richtig"

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = admin_change_product_route(guitar.id)

    response = login_admin_test_client.post(route,data = {
        "product-name":new_guitar.name,
        "price":"",
        "stock":f'{new_guitar.stock}',
        "description":new_guitar.description,
        "stripe_price_id":new_guitar.stripe_price_id,
    },follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data


def test_change_product_int_not_valid(test_app:Flask,login_admin_test_client:FlaskClient,admin_change_product_route,new_guitar):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` input data is string, but price not digit
        :param:`THEN` check if flash_message correct
    '''

    expected_flash_message = b"Geben Sie bei Preis und Anzahl nur Zahlen ein"

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = admin_change_product_route(guitar.id)

    response = login_admin_test_client.post(route,data = {
        "product-name":new_guitar.name,
        "price":"892A",
        "stock":f'{new_guitar.stock}',
        "description":new_guitar.description,
        "stripe_price_id":new_guitar.stripe_price_id,
    },follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data


def test_change_product_img_not_valid(test_app:Flask,login_admin_test_client:FlaskClient,admin_change_product_route,new_guitar):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` input data is string,but imgs not valid
        :param:`THEN` check if flash_message correct
    '''

    expected_flash_message = b"Bilder nicht"

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = admin_change_product_route(guitar.id)

    with open("./tests/test_files/test_pdf.pdf","rb") as f:
        file = FileStorage(f)

        response = login_admin_test_client.post(route,data = {
            "product-name":new_guitar.name,
            "price":f"{new_guitar.price}",
            "stock":f'{new_guitar.stock}',
            "description":new_guitar.description,
            "stripe_price_id":new_guitar.stripe_price_id,
            "img-0":file
        },follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data


def test_delete_product_not_existing(login_admin_test_client:FlaskClient,admin_delete_product_route):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` a id gets passed, but the product doesn't exist
        :param:`THEN` check if 404 error raised
    '''

    not_existing_id = 32323
    route = admin_delete_product_route(not_existing_id)

    response = login_admin_test_client.get(route,follow_redirects = True)

    assert response.status_code == 404


def test_delete_product(test_app:Flask,login_admin_test_client:FlaskClient,admin_delete_product_route,new_guitar):
    '''
        :param:`GIVEN` an admin route
        :param:`WHEN` an existing id gets passed
        :param:`THEN` check if product deleted successfully
    '''

    expected_flash_message = b'Produkt erfolgreich'

    with test_app.app_context():
        guitar = Guitar.get_by_name(new_guitar.name)

    route = admin_delete_product_route(guitar.id)

    response = login_admin_test_client.get(route,follow_redirects = True)

    assert response.status_code == 200
    assert expected_flash_message in response.data 

    # check if deleted
    assert os.path.exists("./website/static/Bilder/Produktbilder/Test") == False

    # recreate the folder structure ---------------

    folder_path = "./tests/test_files/img_of_Test_model"

    new_folder_path = "./website/static/Bilder/Produktbilder/Test"

    ext_list = ["0.png","1.JPG","2.JPG","3.png","4.JPG"]

    # add guitar and images back to db/storage
    guitar = TestDataSetup().create_guitar()

    with test_app.app_context():

        db.session.add(guitar)
        db.session.commit()

        # loop through list
        for ext in ext_list:
            number = ext.split(sep=".")[0]

            recreate_image_in_folder(f"{folder_path}/{ext}",number,new_guitar.name)
            assert os.path.exists(f"{new_folder_path}/{ext}") == True

        assert Guitar.check_guitar_exists_by_name(new_guitar.name) == True
