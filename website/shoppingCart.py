from .models import Guitar
from abc import ABC, abstractmethod

class CartManager:

    '''
        Manages the Products in the shopping_cart
    '''

    def create_product_dict(self,product_id:int,quantity:int) -> dict: 
        '''
            Creates and returns the dictionary of a product, how one gets saved.
            Example: `{'id':<product_id>,'quantity':<quantity>}`
            :param: `product_id` is the id of a product
            :param: `quantity` is the quantity of the product
        '''

        return {"id":product_id,"quantity":quantity}
        

    def add_product(self,product_id:int,shopping_cart:list[dict]) -> list[dict]:
        '''
            Adds a product, by its id to the shopping cart
            Returns the new cart, as a list of dictionaries
            :param: `product_id` is the product Id
            :param: `shopping_cart` is a list of dictonaries
        '''
        # if list is None, create it
        if shopping_cart == None:
            shopping_cart = []

        #if product not in cart, add it
        if not self.check_product_in_order(product_id,shopping_cart) or shopping_cart == []:

            new_product = self.create_product_dict(product_id,1)
            
            shopping_cart.append(new_product)

            return shopping_cart

        else:   #product is already in cart, increase quantity
            return self.increase_quantity(product_id,shopping_cart)


    def check_product_in_order(self,product_id:int,shopping_cart:list[dict]) -> bool:
        '''
            Checks if the product, with the given Id is already in the order
            Returns a boolean
            :param: `product_id` is the id of the product, which is beeing checked
            :param: `shopping_cart` is a list of dictonaries
        '''

        #loop through the cart and get every product
        # product is a dictonary with id and quantity
        for product in shopping_cart:
            if product["id"] == product_id:
                return True
            
        return False


    def increase_quantity(self,product_id:int,shopping_cart:list[dict]) -> list[dict]:
        '''
            increases the quantity of the product with the given id
            Returns the new cart
            :param: `product_id` is the id of the product
            :param: `shopping_cart` is a list of dictionaries
        '''

        if self.check_product_in_order(product_id,shopping_cart):
            #get each dict which is in the list
            for product in shopping_cart:
                #check the id
                if product["id"] == product_id:
                    #increase the quantity
                    product["quantity"] += 1 

        else:
            raise ValueError(f"Can't increase quantity of product with id {product_id}, which is not in shopping cart")

        return shopping_cart 
    

    def set_quantity(self,product_id:int,shopping_cart:list[dict],new_quantity:int) -> list[dict]:
        '''
            Sets the quantity of a product in the shopping_cart
            Returns the new list.
            If `new_quantity` equals 0, then the product gets deleted
            :param: `product_id` is the id of the product
            :param: `shopping_cart` is a list of dictionaries
            :param: `new_quantity` is the new quantity of the product
        '''

        # check if product in cart
        if self.check_product_in_order(product_id,shopping_cart):

            # get each dict which is in the list
            for product in shopping_cart:
                #check the id
                if product["id"] == product_id:
                    
                    if new_quantity == 0:
                        # delete product and get new list
                        shopping_cart = self.delete_product(product_id,shopping_cart)

                    else:
                        product["quantity"] = new_quantity

        else:
            # if not in cart add it
            new_product = self.create_product_dict(product_id,new_quantity)
            shopping_cart.append(new_product)

        return shopping_cart


    def delete_product(self,product_id:int,shopping_cart:list[dict]) -> list[dict]:
        '''
            Deletes a product from the shopping cart, based on its id
            Returns the new shopping cart as list
            :param: `product_id` is the id of the product
            :param: `shopping_cart` is a list of dictionaries
        '''

        # check if product in cart
        if self.check_product_in_order(product_id,shopping_cart):
            
            #create new cart
            new_cart = []

            # get each product
            for product in shopping_cart:

                # if product_id not equal to deleted one, add it to new_cart, otherwise don't
                # -> creates a new list without the deleted one  -> deletes the product with given id
                if product["id"] != product_id:

                    new_product = self.create_product_dict(product["id"],product["quantity"])

                    new_cart.append(new_product)

            return new_cart
        
        #returns it, if product with given id is not in the cart
        return shopping_cart


    def calculate_total_cart_price(self,shopping_cart:list[dict]) -> int:
        '''
            Calculates the total price of the products in the shopping cart;
            Returns an int
            :param: `shopping_cart` is a list of dictionaries
        '''

        total_price = 0

        #check if shopping cart not empty
        if shopping_cart != None and shopping_cart != []:

            #get each product
            for product_dict in shopping_cart:

                # get product
                product = Guitar.query.filter_by(id = product_dict["id"]).first()

                # add price of product times it's quantity
                total_price += product.price * product_dict["quantity"]

        return total_price
    


class CartConverter(ABC):
    '''
        Converts the format of the shopping cart
        Is a abstract overclass
    '''

    @abstractmethod
    def convert_dict(self,product_id:int,quantity:int) -> (dict | None):
        '''
            Returns a dictionary, if product exists, in a different format
            :param: `product_id` is the id of the product
            :param: `quantity` is the product quantity in the shopping cart
        '''
        

    @abstractmethod
    def convert_all_dicts(self,shopping_cart:list[dict]) -> (list[dict] | None):
        '''
            Returns a list, if cart not empty, made up of dictionaries
            :param: `shopping_cart` is a list of dictionaries, which have the following structure:
            `product = {"id": <product_id> , "quantity": <quantity>}
        '''
        


class StripeCartConverter(CartConverter):

    '''
        Class for converting cart dictionaries to stripe format
    '''

    def convert_dict(self,product_id:int,quantity:int) -> (dict | None):
        '''
            Returns a dictionary, if product exists, for stripe checkout session
            Example Structure: `product = {"price": <stripe_price_id>,"quantity": <quantity>}`
            :param: `product_id` is the id of the product
            :param: `quantity` is the product quantity in the shopping cart
        '''
        product = Guitar.query.filter_by(id = product_id).first()

        if product:

            stripe_product_dict = {
                "price": product.stripe_price_id,
                "quantity":quantity
            }

            return stripe_product_dict
        
    
    def convert_all_dicts(self,shopping_cart: list[dict]) -> list[dict] | None:
        '''
            Returns a list, if cart not empty, made up of dictionaries, for stripe checkout.
            New Example Structure of one dictionary: 
            `product = {"price": <stripe_price_id>,"quantity": <quantity>}`
            :param: `shopping_cart` is a list of dictionaries, which have the following structure:
            `product = {"id": <product_id> , "quantity": <quantity>}
        '''

        #check if not empty and not none
        if shopping_cart != [] and shopping_cart != None:

            new_list = []

            # loop throught the individual product dicts
            for product_dict in shopping_cart:

                new_dict = self.convert_dict(product_dict["id"],product_dict["quantity"])

                new_list.append(new_dict)

            return new_list