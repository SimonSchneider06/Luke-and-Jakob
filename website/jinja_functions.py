from .models import Guitar

def get_product_by_id(id:int) -> Guitar:
    ''' Returns product by product id
        @param id: product id
    '''
    product = Guitar.query.filter_by(id = id).first()
    return product
