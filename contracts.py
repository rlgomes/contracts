"""
This library is a very simple and straightforward way of implementing contracts
in python using decorators. I did have a look at a few other contract libraries 
and found that they were either not very pythonic or decided to use strings to 
encode the contract logic which makes it horrible to debug or even write your 
contracts cleanly.
"""
import inspect

CONTRACTS_ENABLED = False

def __identity(function):
    """
    identify function just returns the same function 
    """
    return function

def __bind(fromfunction, tofunction):
    """
    binds the required elements of a fromfunction to the tofunction
    """
    tofunction.__name__ = fromfunction.__name__
    tofunction.__doc__ = fromfunction.__doc__
#    tofunction.__dict__.update(fromfunction.__dict__)
    return tofunction

def __remap_pre(decorated_function, contract_function, message):
    """
    remap function for the pre contract
    """
    def new_f(*args, **kwds):
        """
        pre contract wrapper function
        """
        assert contract_function(*args, **kwds), message
        return decorated_function(*args, **kwds)
                    
    return __bind(decorated_function, new_f)      

def __remap_post(decorated_function, contract_function, message):
    """
    remap function for the post contract
    """
    def new_f(*args, **kwds):
        """
        post contract wrapper function
        """
        result = decorated_function(*args, **kwds)
        assert contract_function(result), message
        return result
    
    return __bind(decorated_function, new_f)      

def __remap_inv(_, decorated_function, contract_function, message):
    """
    remap function for the invariant contract
    """
    def new_f(*args, **kwds):
        """
        invariant wrapper function
        """
        # in a class method the first argument is the self ;)
        self_ref = args[0]
        assert contract_function(self_ref), message
        result = decorated_function(*args, **kwds)
        assert contract_function(self_ref), message
        return result
    
    return __bind(decorated_function, new_f)      

def __remap_class(obj, create_function, contract_function, message):
    """
    remap class for the invariant contract
    """
    members = inspect.getmembers(obj)
          
    for (name, member) in members:
        # or inspect.isbuiltin(member) or inspect.isroutine(member):
        if inspect.ismethod(member): 
            newfunc = create_function(obj, member, contract_function, message)
            setattr(obj, name, newfunc)
            
    func =  create_function(obj, obj.__setattr__, contract_function, message)
    setattr(obj, "__setattr__", func)
            
    return obj

def post(contract_function, message=None):
    """
    This defines a contract which is validated when the function decorated with
    this decorator is returning from execution. The function you provide will 
    receive the return value of the function that was decorated and you can use
    that during your post-validation.
    
    Note: Turn contracts on by setting the contracts.CONTRACTS_ENABLED to True
    
    function - the function to call once the currently decorated function has 
               finished executing and provide the return value to this function.
               
    message  - message to print when this post-condition fails and contracts are
               enabled.
               
    """
    if CONTRACTS_ENABLED:
        if message == None :
            message = "post-condition %s has failed" % contract_function
        
        def check_post(decorated_element):
            """
            post condition check wrapper function
            """
            if inspect.isfunction(decorated_element):
                return __remap_post(decorated_element,
                                    contract_function,
                                    message)
            else:
                raise Exception("Only classes and functions can " + 
                                "have post contracts")
            
        return check_post
    else:
        return __identity

def pre(contract_function, message=None):
    """
    This defines a contract which is validated when the function decorated with
    this decorator is about to execute. The function you provide will execute
    with the same arguments that are passed to the decorated function. 

    Note: Turn contracts on by setting the contracts.CONTRACTS_ENABLED to True
    
    function - the function to call once the currently decorated function is 
               about to execute.
               
    message  - message to print when this pre-condition fails and contracts are
               enabled.

    """
    if CONTRACTS_ENABLED:
        if message == None :
            message = "pre-condition %s has failed" % contract_function
            
        def check_pre(decorated_element):
            """
            pre condition check wrapper function
            """
            if inspect.isfunction(decorated_element):
                return __remap_pre(decorated_element,
                                   contract_function,
                                   message)
            else:
                raise Exception("Only functions can have pre contracts")
            
        return check_pre
    else:
        return __identity

def inv(contract_function, message=None):
    """
    This defines a contract which is validated when any method is called on a 
    class decorated with this decorator. This means the invariant contract will 
    be executed before the class method is executed and after it has exited. 
    The argument provided to the contract function is always the instance of the
    object being handled at the moment.

    Note: Turn contracts on by setting the contracts.CONTRACTS_ENABLED to True
    
    class - the function to call once the currently decorated function is 
            about to execute.
               
    message  - message to print when this pre-condition fails and contracts are
               enabled.

    """
    if CONTRACTS_ENABLED:
        if message == None :
            message = "inv-condition %s has failed" % contract_function
            
        def check_invariant(decorated_element):
            """
            invariant check wrapper function
            """
            if inspect.isclass(decorated_element):
                return __remap_class(decorated_element,
                                    __remap_inv,
                                    contract_function,
                                    message)
            else:
                raise Exception("Only classes can have invariant contracts")
            
        return check_invariant
    else:
        return __identity
