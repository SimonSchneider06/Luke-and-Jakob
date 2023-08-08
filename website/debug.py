

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