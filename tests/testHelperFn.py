from werkzeug.datastructures import FileStorage
from website.ImageManager import ImageManager
from website.data_validation import check_list_of_str_correct,check_str_correct

def recreate_image_in_folder(img_path:str,number:int,product_name:str):
    '''
        Recreates the image back to the folder
        :param: `img_path` is the path of the image, which should be saved back to 
        the Produktbilder, because of Test purposes
        :param: `number` is the number, by which the img should be saved
        :param: `product_name` is the name of the product
    '''

    with open(img_path, "rb") as f:
        file = FileStorage(f)
        ImageManager().save_image_by_product_name_and_number(file,number,product_name)


def image_path_setup(img_list:list[str],folder_path:str) -> (tuple[list, str] | None):
    '''
        Returns a list with image paths and the path of the front img
        :param: `ext_list` is a list with the image extensions
        :param: `folder_path` is the path where those images are stored
    '''

    if check_list_of_str_correct(img_list) and check_str_correct(folder_path):

        return_list = []

        # get front_img separat
        images = img_list[1:]

        # loop through img_list
        for img in images:
            path = f'{folder_path}/{img}'
            return_list.append(path)

        front_img_path = f'{folder_path}/{img_list[0]}'

        return return_list,front_img_path
        