import pytest
from website.debug import check_str_input_correct


def test_check_str_input_correct():
    '''
        `GIVEN` a ImageManager method
        `WHEN` a correct String, argument name and function gets passed 
        `THEN` check if True gets returned
    '''

    assert check_str_input_correct("test_value","test_arg","ImageManager().check_img_ext") == True


def test_check_str_input_function_invalid():
    '''
        `GIVEN` a ImageManager method
        `WHEN` a valid string, valid argument name and function, not as string, gets passed 
        `THEN` check if Error raised
    '''

    # 
    with pytest.raises(TypeError):
        check_str_input_correct("test_string","test_arg",0)




def test_check_str_input_string_invalid():
    '''
        `GIVEN` a ImageManager method
        `WHEN` a string invalid(empty or not string), argument name and function both valid strings gets passed 
        `THEN` check if Errors raised
    '''

    # not string
    with pytest.raises(TypeError):
        check_str_input_correct(0,"test_arg","test_function")

    # empty string
    with pytest.raises(ValueError):
        check_str_input_correct("","test_arg","test_function")


def test_check_str_input_argument_name_invalid():
    '''
        `GIVEN` a ImageManager method
        `WHEN` a valid string, argument name invalid(not string and empty string) and function valid strings gets passed 
        `THEN` check if Errors raised
    '''

    # not string
    with pytest.raises(TypeError):
        check_str_input_correct("test_string",0,"test_function")

    # empty string
    with pytest.raises(ValueError):
        check_str_input_correct("test_string","","test_function")
