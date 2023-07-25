from .models import Guitar

class CartManager:

    '''
        Manages the Products in the shopping_cart
    '''

    def add_product(self,product_id:int,shopping_cart:list) -> list:
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

            new_product = {
                "id": product_id,
                "quantity":1,
            }
            
            shopping_cart.append(new_product)

            return shopping_cart

        else:   #product is already in cart, increase quantity
            return self.increase_quantity(product_id)


    def check_product_in_order(self,product_id:int,shopping_cart:list) -> bool:
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


    def increase_quantity(self,product_id:int,shopping_cart:list) -> list:
        '''
            increases the quantity of the product with the given id
            Returns the new cart
            :param: `product_id` is the id of the product
            :param: `shopping_cart` is a list of dictionaries
        '''

        #get each dict which is in the list
        for product in shopping_cart:
            #check the id
            if product["id"] == product_id:
                #increase the quantity
                product["quantity"] += 1 

        return shopping_cart 
    

    def set_quantity(self,product_id:int,shopping_cart:list,new_quantity:int) -> list:
        '''
            Sets the quantity of a product in the shopping_cart
            Returns the new list.
            If `new_quantity` equals 0, then the product gets deleted
            :param: `product_id` is the id of the product
            :param: `shopping_cart` is a list of dictionaries
            :param: `new_quantity` is the new quantity of the product
        '''

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

        return shopping_cart


    def delete_product(self,product_id:int,shopping_cart:list) -> list:
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

                    new_product = {
                        "id": product["id"],
                        "quantity": product["quantity"]
                    }

                    new_cart.append(new_product)

            return new_cart
        
        #returns it, if product with given id is not in the cart
        return shopping_cart


    def calculate_total_cart_price(self,shopping_cart:list) -> int:
        '''
            Calculates the total price of the products in the shopping cart;
            Returns an int
            :param: `shopping_cart` is a list of dictionaries
        '''

        #check if shopping cart not empty
        if shopping_cart != None and shopping_cart != []:

            total_price = 0

            #get each product
            for product_dict in shopping_cart:

                # get product
                product = Guitar.query.filter_by(id = product_dict["id"]).first()

                # add price of product times it's quantity
                total_price += product.price * product_dict["quantity"]

        return total_price