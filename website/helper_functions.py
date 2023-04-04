from os import walk
from flask import current_app as app

def add_cart_item(cart, add_product_id):

    #new cart
    new_cart = []
    #variable, which checks if the product already is in the shopping_cart
    is_new_id = True

    #loops through the cart to get each list
    for product_list in cart:
        #first item = product_id, second = menge
        #if new item is already in cart, add 1 to menge
        if product_list[0] == add_product_id:
            product_list[1] += 1
            is_new_id = False
        #append list
        new_cart.append(product_list)

    #if id isnt in cart, because if statement from above never executed, add it
    if is_new_id:
        new_cart.append([add_product_id,1])

    return new_cart


#------gets file path -------------------------------------

def get_file_by_product_name(product_name,img_number):

    folder = app.config["UPLOAD_PATH"] + f"/{product_name}"
    
    path = f"Bilder/Produktbilder/{product_name}"
    
    for (_, __ , filenames) in walk(folder):
        for file in filenames:
            file_name = file.split(".")[0]

            #filename is a string !!!!!!
            if file_name == f"{img_number}":
                full_path = path + f"/{file}"
    
    return full_path
