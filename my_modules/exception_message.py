import inspect

#exception message main
class exception_message(Exception):
    
    def main(ex, self=None, name_ex=''):
        
        #final string init
        
        ex_string = '*'*3+'file name('+inspect.stack()[1].filename+') - '
    
        #if name_ex exists, write name_ex without adding location information, etc.
        if name_ex:
            ex_string = str(ex)
        else:
            
            #calling class, function/method 
            function_name = inspect.stack()[1].function
            #if class
            if self:
                ex_string += 'class name('+self.__class__.__name__+') - '
            ex_string += 'function/method name('+str(function_name)+') - '+str(ex)+'*'*3
                
        return ex_string


#exception message clear
class exception_message_clear(Exception):
    
    def main(ex):
        ex_string = str(ex)
        return ex_string
    
#exception message empty
class exception_empty(Exception):   
    pass