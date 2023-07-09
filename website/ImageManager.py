from flask import current_app as app
from flask import abort
import os
#import imghdr to validate image file and size
import imghdr
import shutil
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage 

class ImageManager:

    def get_image_path_by_product_name_and_number(self,product_name:str,img_number:int) -> (str | None):
        '''
            Returns the file path of a product-image by a given number
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

        if file_path == None or type(file_path) != str:
            raise TypeError("file_path should be of type String")

        if file_path == "":
            raise ValueError("file_path shouldn't be an empty String")

        file_path_secure = secure_filename(file_path)
        # return the last part of the splitted text
        
        return os.path.splitext(file_path_secure)[1]


    def get_folder_path_by_product_name(self,product_name:str) -> str:
        
        '''
            Returns the folder path of a product, by it's name
            Path Structure: './website/static/Bilder/Produktbilder/<product_name>'
            :param: `product_name` name of the product
        '''

        if product_name == "":
            raise ValueError("product_name shouldn't be an empty String")
        
        if product_name == None or type(product_name) != str:
            raise TypeError("product_name should be of type String")

        return f'{app.config["UPLOAD_PATH"]}/{product_name}'


    def check_img_ext(self,img_path:str) -> bool:

        '''
            Checks if the extension of the image is valid or not
            :param: `img_path` the path, which should be checked
        '''

        #check if valid input
        if img_path == None or type(img_path) != str:
            raise TypeError("Img_path should be of type String")
        
        if img_path == "":
            raise ValueError("img_path shouldn't be an empty String")
        
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
        format = imghdr.what(None,header)
        if not format:
            return False
        stream_ext =  "." + (format if format != "jpeg" else "JPG")

        if stream_ext == self.get_file_path_ext(image.filename):
            return True


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

        if path == "":
            raise ValueError("Path shouldn't be an empty string")
        
        if path == None or type(path) != str:
            raise TypeError("Path should be of type String")

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

            path_to_save = f'{folder_path}/{number}.{img_ext}'

            # checks if the path exists

            image.save(path_to_save)


    def delete_directory_by_product_name(self,product_name:str) -> None:
        '''
            Deletes the folder directory and it's content from a given product
            :param: `product_name` name of the product
        '''

        folder_path = self.get_folder_path_by_product_name(product_name)
        shutil.rmtree(folder_path)
