from flask import session
from .models import Guitar


def get_product_by_id(id:int) -> Guitar:
    ''' Returns product by product id
        @param id: product id
    '''
    product = Guitar.query.filter_by(id = id).first()
    return product


def calculate_total_shopping_price() -> int:
    '''
        Calculate the total price of all items stored in session["cart"], 
        the shopping cart of the user
    '''
    
    total_price = 0

    if session["cart"]:
        
        #loop through the product_lists
        for product_list in session["cart"]:
            
            #get product
            product = Guitar.query.filter_by(id = product_list[0]).first()

            #price of product * menge of product = price
            price = product.price * product_list[1]

            total_price += price

    return total_price