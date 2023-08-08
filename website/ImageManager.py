from flask import current_app as app
import os
import shutil
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage 
from sqlalchemy import select
from . import db 
from .models import Guitar
import magic   # for image stream validation
from .debug import check_str_input_correct

class ImageManager:
    '''
        Manages the Images
    '''

    def get_image_path_by_product_name_and_number(self,product_name:str,img_number:int) -> (str | None):
        '''
            Returns the file path of a product-image by a given number.
            Returns None if product_name doesn't exist or file by number doens't exist
            :param: `product_name` the name of the product
            :param: `img_number` the number of the searched image
        '''

        folder = self.get_folder_path_by_product_name(product_name)
    
        path = f"Bilder/Produktbilder/{product_name}"
        
        for (_, __ , filenames) in os.walk(folder):
            for file in filenames:
                file_name = file.split(".")[0]

                #filename is a string !!!!!!
                if file_name == f"{img_number}":
                    full_path = path + f"/{file}"
                    return full_path
        
        return None
        

    def get_file_path_ext(self,file_path:str) -> str:

        '''
            Return the extension of a given filepath
            :param: `file_path` is a string
        '''
        
        #checks input string to type/value errors
        if check_str_input_correct(file_path,"file_path","self.get_file_path_ext"):

            file_path_secure = secure_filename(file_path)
            # return the last part of the splitted text
            
            ext = os.path.splitext(file_path_secure)[1]

            if ext != "":
                return ext
            
            else:
                raise ValueError("file_path should have an extension. Don't pass a path without one as argument")     


    def get_folder_path_by_product_name(self,product_name:str) -> str:
        
        '''
            Returns the folder path of a product, by it's name
            Path Structure: './website/static/Bilder/Produktbilder/<product_name>'
            :param: `product_name` name of the product
        '''

        if check_str_input_correct(product_name,"product_name","get_folder_path_by_product_name"):
        
            # check if product exists
            if not Guitar().check_guitar_exists_by_name(product_name):

                raise ValueError(f"Product with name {product_name} does not exist")
            
            else:
                return f'{app.config["UPLOAD_PATH"]}/{product_name}'
            

    def check_img_ext(self,img_path:str) -> bool:

        '''
            Checks if the extension of the image is valid or not
            :param: `img_path` the path, which should be checked
        '''

        #check if valid input
        if check_str_input_correct(img_path,"img_path","check_img_ext"):
        
            #get the extension
            path_ext = self.get_file_path_ext(img_path)

            if path_ext not in app.config["UPLOAD_EXTENSIONS"]:
                return False
            
            return True
    

    def check_image_stream(self,image: FileStorage) -> bool:
        '''
            Verifies the image by looking at its file Stream
            :param: `image` is of type FileStorage from Flask
        '''

        if image == None or type(image) != FileStorage:
            raise TypeError("image should be of Type FileStorage")
        
        stream = image.stream
        header = stream.read(512)
        stream.seek(0)
        format = magic.from_buffer(header)

        if not format:
            return False
        
        else:

            stream_ext = ""
        
            if "PNG image data" in format:# or "JPEG image data":
                stream_ext = ".png"

            if "JPEG image data" in format:
                stream_ext = ".JPG"

            if stream_ext != "":

                if stream_ext == self.get_file_path_ext(image.filename):
                    return True
            else:
                return False


    def verify_image(self,image:FileStorage) -> bool:

        '''
            head level function: verifies the image
            :param: `image` is of type FileStorage, from Flask
        '''

        if image == None or type(image) != FileStorage:
            raise TypeError("Image should be of type FileStorage")

        if self.check_img_ext(image.filename) and self.check_image_stream(image):
            return True
        else:
            return False
                    

    def create_folder_structure(self,path:str) -> None:

        '''
            Creates a folder structure if it doesn't exist already
            :param: `path` is the folder_path which gets created
        '''

        if check_str_input_correct(path,"path","create_folder_structure"):

            #checks if path exists already
            if not os.path.exists(path):
                os.mkdir(path)


    def save_image_by_product_name_and_number(self,image:FileStorage,number:int,product_name:str) -> None:

        '''
            Saves the image according to the product it belongs to and the number it has; 
            :param: `image` is of type FileStorage, from Flask
            :param: `number` is the number by which it should be stored
            :param: `product_name` is the name of the product the image belongs to 
        '''

        if self.verify_image(image):
            img_ext = self.get_file_path_ext(image.filename)

            folder_path = self.get_folder_path_by_product_name(product_name)

            self.create_folder_structure(folder_path)

            path_to_save = f'{folder_path}/{number}{img_ext}'

            # checks if the path exists

            image.save(path_to_save)


    def delete_directory_by_product_name(self,product_name:str) -> None:
        '''
            Deletes the folder directory and it's content from a given product
            :param: `product_name` name of the product
        '''

        if check_str_input_correct(product_name,"product_name","delete_directory_by_product_name"):

            folder_path = self.get_folder_path_by_product_name(product_name)
            shutil.rmtree(folder_path)
    