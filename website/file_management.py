from flask import current_app as app
from flask import abort
import os
#import imghdr to validate image file and size
import imghdr
import shutil
from werkzeug.utils import secure_filename

#------gets file path -------------------------------------

def get_file_path_by_product_name(product_name,img_number) -> (str | None):

    folder = app.config["UPLOAD_PATH"] + f"/{product_name}"
    
    path = f"Bilder/Produktbilder/{product_name}"
    
    for (_, __ , filenames) in os.walk(folder):
        for file in filenames:
            file_name = file.split(".")[0]

            #filename is a string !!!!!!
            if file_name == f"{img_number}":
                full_path = path + f"/{file}"
                return full_path
    
    return None

#check and save img
def check_save_img(image,guitar_name,number):
    if image != None:
    
    #checks if filename not empty, so if file got recieved
        if secure_filename(image.filename) != "":
            #save image
            save_image_with_number(image,guitar_name,number)


#save images by their specific number to not overwrite existing ones
def save_image_with_number(image, guitar_name,number):

    #number = image.split("_")[1]    # image = img_0 ; so get the 0
    file_ext = os.path.splitext(image.filename)[1]

    # if not valid abort  -- "\" makes the if go over the next line
    if file_ext not in app.config["UPLOAD_EXTENSIONS"] or file_ext != validate_image(image.stream):
        abort(400)

    file_path = app.config["UPLOAD_PATH"] + f"/{guitar_name}/{number}.{file_ext}"

    image.save(file_path)

# ------------------------------validate image function----------------------

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None,header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "JPG")

#saves , and checks images from array---------------------------------------------------------

def save_uploaded_img(img_list,guitar_name):
    #create count number
    i = 0

    #loops through the uploaded_images array
    for uploaded_img in img_list:
        #makes the filename secure

        filename = secure_filename(uploaded_img.filename)
        #filename = uploaded_img.filename

        #if filename is empty -> no file received so if not empty -> file received
        if filename != "":
            
            #splits the extension of the filename to look if its valid or not 
            file_ext = os.path.splitext(filename)[1]
            # print(file_ext)

            # if not valid abort  -- "\" makes the if go over the next line
            if file_ext not in app.config["UPLOAD_EXTENSIONS"] or file_ext != validate_image(uploaded_img.stream):
                abort(400)

            new_folder_path = app.config["UPLOAD_PATH"] + f"/{guitar_name}"
            if not os.path.exists(new_folder_path):
                os.mkdir(new_folder_path)

            #save img in ./website/static/Bilder/Productbilder/name of the guitar so there cant be duplicates
            path = os.path.join(new_folder_path,str(i) + file_ext )
            uploaded_img.save(path)
            #adding one to image count
            i += 1 

    return new_folder_path if i >= 1 else None



def del_dir_from_guitar_name(guitar_name:str) -> None:

    '''Delete directory of image by guitar'''

    #gets path
    img_path = app.config["UPLOAD_PATH"] + f"/{guitar_name}"
    #Deletes directory with imgs
    shutil.rmtree(img_path)