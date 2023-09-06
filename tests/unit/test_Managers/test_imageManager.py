import pytest
from werkzeug.datastructures import FileStorage
import os
import shutil

from website.ImageManager import ImageManager
from tests.testHelperFn import recreate_image_in_folder


def test_get_image_path_by_product_name_and_number(new_guitar,test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a image should be found by product name and image number
        `THEN` check if path gets returned 
    '''

    product_name = new_guitar.name

    with test_app.app_context():
        assert ImageManager().get_image_path_by_product_name_and_number(product_name,0) == "Bilder/Produktbilder/Test/0.png"
        assert ImageManager().get_image_path_by_product_name_and_number(product_name,3) == "Bilder/Produktbilder/Test/3.png"


def test_get_image_path_by_product_name_and_number_name_is_invalid(test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a image should be found by product name, which doesn't exist and image number
        `THEN` check if ValueError gets returned
    '''

    product_name = "notExisting"

    with test_app.app_context():

        with pytest.raises(ValueError):
            ImageManager().get_image_path_by_product_name_and_number(product_name,0)


def test_get_image_path_by_product_name_and_number_invalid_number(new_guitar,test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a image should be found by product name and (image number, which doesn't exist)
        `THEN` check if None gets returned 
    '''

    product_name = new_guitar.name

    with test_app.app_context():
        assert ImageManager().get_image_path_by_product_name_and_number(product_name,7) == None


def test_get_image_path_by_product_name_and_number_number_ofType_str(new_guitar,test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a image should be found by product name and image number,one valid, one invalid, both with wrong type of string
        `THEN` check if path gets returned 
    '''
    product_name = new_guitar.name

    with test_app.app_context():
        assert ImageManager().get_image_path_by_product_name_and_number(product_name,"3") == "Bilder/Produktbilder/Test/3.png"
        assert ImageManager().get_image_path_by_product_name_and_number(product_name,"7") == None


def test_get_file_path_ext():
    '''
        `GIVEN` a ImageManager method
        `WHEN` a file extension should be found by file path
        `THEN` check if extension gets returned
    '''

    assert ImageManager().get_file_path_ext("Bilder/Produktbilder/Test/3.png") == ".png"
    assert ImageManager().get_file_path_ext("3.png") == ".png"


def test_get_file_path_ext_file_path_no_extension():
    '''
        `GIVEN` a ImageManager method, the file extension should be found
        `WHEN` when the file_path doesn't have an extension, so a folder path gets returned
        `THEN` check Value error gets raised
    '''

    with pytest.raises(ValueError):
        ImageManager().get_file_path_ext("Bilder/Produktbilder/Test/")

    with pytest.raises(ValueError):
        ImageManager().get_file_path_ext("Bilder/Produktbilder/Test/3")


def test_get_folder_path_by_product_name(new_guitar,test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` the product name is an existing, valid name
        `THEN` check if returned correctly
    '''

    product_name = new_guitar.name

    with test_app.app_context():

        assert ImageManager().get_folder_path_by_product_name(product_name) == f"./website/static/Bilder/Produktbilder/{product_name}"


def test_get_folder_path_by_product_name_name_not_existing(test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` the product name is a not existing, invalid name
        `THEN` check if Value Error gets raised
    '''

    with test_app.app_context():

        with pytest.raises(ValueError):
            ImageManager().get_folder_path_by_product_name("NotExisting")


def test_check_img_ext(test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a image_path with valid extension gets passed as argument
        `THEN` check if returned True
    '''

    with test_app.app_context():

        assert ImageManager().check_img_ext("Bilder/Produktbilder/Test/0.png") == True


def test_check_img_ext_not_valid(test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a image_path with invalid extension gets passed as argument
        `THEN` check if returned False
    '''

    with test_app.app_context():

        assert ImageManager().check_img_ext("Bilder/Produktbilder/Test/0.mp4") == False


def test_check_image_stream():

    '''
        `GIVEN` a ImageManager method
        `WHEN` a valid image gets passed as argument
        `THEN` check if returnes True
    '''

    # get file of type Filestorage
    file = None
    
    with open("./website/static/Bilder/Produktbilder/Test/1.JPG","rb") as f:
        file = FileStorage(f)
        assert ImageManager().check_image_stream(file) == True

    with open("./website/static/Bilder/Produktbilder/Test/0.png","rb") as f:
        file = FileStorage(f)
        assert ImageManager().check_image_stream(file) == True


def test_check_image_stream_invalid_file():

    '''
        `GIVEN` a ImageManager method
        `WHEN` a invalid file gets passed as argument
        `THEN` check if returnes True
    '''

    # get file of type Filestorage
    file = None
    
    with open("./tests/test_files/test_pdf.pdf","rb") as f:
        file = FileStorage(f)
        assert ImageManager().check_image_stream(file) == False


def test_check_image_stream_invalid_input_type():
    '''
        `GIVEN` a ImageManager method
        `WHEN` a argument of invalid type, for example str gets passed
        `THEN` check if TypeError gets raised
    '''

    with pytest.raises(TypeError):
        ImageManager().check_image_stream("test_str")    


def test_verify_image(test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a valid image gets passed as argument
        `THEN` check if returned True
    '''

    file = None

    with test_app.app_context():

        with open("./website/static/Bilder/Produktbilder/Test/0.png","rb") as f:

            file = FileStorage(f)
            assert ImageManager().verify_image(file) == True


def test_verify_image_invalid_file(test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a file of wrong type, for example pdf gets passed
        `THEN` check if False gets returned
    '''

    file = None

    with test_app.app_context():

        with open("./tests/test_files/test_pdf.pdf","rb") as f:

            file = FileStorage(f)
            assert ImageManager().verify_image(file) == False


def test_verify_image_invalid_input_type(test_app):
    '''
        `GIVEN` a ImageManager method
        `WHEN` a argument of invalid type, for example str gets passed
        `THEN` check if TypeError gets raised
    '''

    with test_app.app_context():
        with pytest.raises(TypeError):
            ImageManager().verify_image("test_string")


def test_create_folder_structure_and_destroy():
    '''
        `GIVEN` a ImageManager method
        `WHEN` a valid path gets passed
        `THEN` check if path got created
    '''

    # create folder
    ImageManager().create_folder_structure("./tests/test_folder")

    #check if created
    assert os.path.exists("./tests/test_folder") == True

    # remove it again
    shutil.rmtree("./tests/test_folder")

    # check if removed
    assert os.path.exists("./tests/test_folder") == False


def test_save_image_by_product_name_and_number(test_app):
    '''
        `GIVEN` an ImageManager method
        `WHEN` the arguments get passed in correctly, so image, number, product_name
        `THEN` check if image got saved correctly
    '''

    file = None

    with test_app.app_context():

        with open("./tests/test_files/test_img.png","rb") as f:
            file = FileStorage(f)

            ImageManager().save_image_by_product_name_and_number(file,5,"Test")
            assert os.path.exists("./website/static/Bilder/Produktbilder/Test/5.png") == True

            #remove testing image
            os.remove("./website/static/Bilder/Produktbilder/Test/5.png")

            # check if removed
            assert os.path.exists("./website/static/Bilder/Produktbilder/Test/5.png") == False


def test_delete_directory_by_product_name(test_app,new_guitar):
    '''
        `GIVEN` an ImageManager method
        `WHEN` the folder path should be removed, because product gets deleted
        `THEN` check if removed correctly
    '''

    with test_app.app_context():

        ImageManager().delete_directory_by_product_name(new_guitar.name)
        
        # check if deleted
        assert os.path.exists("./website/static/Bilder/Produktbilder/Test") == False

        # recreate the folder structure ---------------

        folder_path = "./tests/test_files/img_of_Test_model"

        new_folder_path = "./website/static/Bilder/Produktbilder/Test"

        ext_list = ["0.png","1.JPG","2.JPG","3.png","4.JPG"]

        # loop through list
        for ext in ext_list:
            number = ext.split(sep=".")[0]

            recreate_image_in_folder(f"{folder_path}/{ext}",number,new_guitar.name)
            assert os.path.exists(f"{new_folder_path}/{ext}") == True
