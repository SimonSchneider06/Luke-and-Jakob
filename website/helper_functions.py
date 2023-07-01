# adds products to shopping cart
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