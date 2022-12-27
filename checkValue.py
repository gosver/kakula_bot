import re

from my_modules.exception_message import exception_message,exception_message_clear



def checkValue(string):

    try:
        
        ERR_DIG = 'Ошибка: Бот забирает значение от начала строки до первого нечисленного символа (+ 20 00 мануар 22.06-28:06) - +2000 '
        
        #sting transform and remove spaces
        string = str(string)
        string = string.replace(' ', '')
        
        #if not digit and minus
        if not string[0].isdigit() and string[0] != '-' and string[0] != '+':
            raise exception_message_clear(exception_message_clear.main(ERR_DIG))
        
        
        #extract string with sign and digit
        regex = "^([0-9-+ ]*)((?=[^\d])|.*$)"
        matches = re.match(regex, string)
        string = matches[0]
        
        #check operand 
        operand = '+'
        if string[0] == '-':
            string = string[1:]
            operand = '-'
        elif string[0] == '+':
            string = string[1:]

        #digit check and send response
        if not string.isdigit():
            raise exception_message_clear(exception_message_clear.main(ERR_DIG))
        else:
            
            return {'value':string, 'operand':operand}

    except exception_message_clear as ex:
        raise ex
    except Exception as ex:
        raise exception_message(exception_message.main(ex))