import string

def check_str_input_correct(string:str,argument_name:str,function_name:str) -> bool:
    '''
        Checks whether the string input is correct or not.
        Returns true or raises errors
        :param: `string` is the string to be checked
        :param: `argument_name` is how the argument is called, in the top level function
        :param: `function_name` is the name of the function, in which it gets called -> for debugging
    '''

    if argument_name == "" or function_name == "":
        raise ValueError(f"{argument_name} argument_name and {function_name} function name shouldn't be empty")
    
    if argument_name == None or type(argument_name) != str:
        raise TypeError(f'{argument_name} argument name should be of type string')
    
    if function_name == None or type(function_name) != str:
        raise TypeError(f'{function_name} function name should be of type string')

    if string == "":
        raise ValueError(f" '{argument_name}' in function 'ImageManager().{function_name}' shouldn't be an emtpy string")
    
    if string == None or type(string) != str:
        raise TypeError(f" '{argument_name}' in function 'ImageManager().{function_name}' should be of type string")
    
    else:
        return True
    

def check_str_correct(string:str) -> bool:
    '''
        Returns True if the input value is a nonempty string, else returns 
        False
    '''
    if type(string) != str or string == None:
        return False
    
    elif string == "":
        return False
    
    else:
        return True
    

def check_list_of_str_correct(liste:list[str]) -> bool:
    '''
        Returns True if all strings in the list are valid, else
        returns False
        :param: `list` is a list of strings
    '''

    #loop through list
    for string in liste:

        # if item not valid returns false
        if check_str_correct(string) == False:
            return False
    
    return True


def check_int_input_correct(number:int) -> bool:
    try:
        int(number)
        return True
    except:
        return False


def convert_rememberMe(rememberMe:str) -> bool:
    '''
        Converts the rememberMe value from a string to a boolean.
        Returns `true` or `false`.
        :param: `rememberMe` is either `on` or `off` 
    '''

    if check_str_correct(rememberMe):

        if rememberMe == "on":
            return True
        else:
            return False
        

def check_password_secure(password:str) -> bool:
    '''
        Takes a Password and checks if it is secure
        Returns True if secure.
        :param: `password` is the password
    '''
    # for a password to be considered secure it should have
    # - more than 8 characters
    # - at least one lowercase letter
    # - at least one uppercase letter
    # - at least one number
    # - at least one punctuation

    #should have more than 8 Characters and be a string
    if len(password) > 8 and check_str_correct(password):

        lowercase = False
        uppercase = False
        number = False
        punctuations = False 
        
        for element in password:
            if element in string.ascii_lowercase:
                lowercase = True
            elif element in string.ascii_uppercase:
                uppercase = True
            elif element in string.digits:
                number = True
            elif element in string.punctuation:
                punctuations = True

        if lowercase == False or uppercase == False or number == False or punctuations == False:
            return False
        else:
            return True
        
    else:
        return False
    

def check_sign_in_data_correct(email:str,password1:str,rememberMe:str) -> str | bool:
    '''
        When data from HTML-Forms gets requested, check if everything is correct
        Returns string with output message to be flashed, e.g. if email exists returns `Emails exists already` and so on
        if the data is correct, return `Data Correct`
        :param: `email` is the email of the User, check if it already exists
        :param: `password1` is the password of the User
        :param: `rememberMe` is either `on` or `off`. See if User wants to stay logged in
    '''

    from .models import User
    
    # check if everything is a nonempty string
    if check_list_of_str_correct([email,password1,rememberMe]) == True:

        # check that email doesn't exist jet
        if User.check_email_exists(email):
            return "Email exists already"
        
        elif check_password_secure(password1) != True:
            return "Password not secure enough, please choose a more secure one"

        else: 
            return True
                    
    else:
        return "Input values are not correct"