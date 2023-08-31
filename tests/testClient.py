from flask.testing import FlaskClient

class CustomClient(FlaskClient):
    '''
        Custom definition of the flask_test_client 
    '''

    def __init__(self,*args,**kwargs):
        self._role = kwargs.pop("role")
        #self.authorisation = kwargs.pop("authorisation")
        super(CustomClient,self).__init__( *args, **kwargs)

    
