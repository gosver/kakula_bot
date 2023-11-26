import telebot
import os
import json

from checkValue import checkValue
from dbOperations import dbOperations
from dotenv import load_dotenv

from my_modules.exception_message import exception_message, exception_message_clear,exception_empty
from my_modules.log import write_log

load_dotenv()
token = os.getenv("TLG_TOKEN")
db = json.loads(os.getenv("DATA_BASE"))
#tuple_of_access = os.getenv("TLG_TUPLE_OF_ACCESS").split(',')

#telegram bot

def telegram_bot(token):
    bot=telebot.TeleBot(token)
    
    #start message
    
    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Ola kakula")
    
    #wait text   
    
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        
        #print(message.from_user.id)
        
        try:
            
            #check_access
            check_access = True
            #for access in tuple_of_access:
            #    if access == str(message.from_user.id):
            #        check_access = True
            #        break
            
            if not check_access:
                raise exception_empty('')
            
            #check value from user
            value_from_user = checkValue(message.text)
            
            #get chat_id
            chat_id = message.chat.id
            
            #check, get value from db
            dbOperation = dbOperations(db)
            dbOperation.connect()
            dbOperation.check_tables()
            dbOperation.select_chatid(chat_id)
            free_count_finish = dbOperation.get_active_status(chat_id)
            if free_count_finish:
                raise exception_message_clear(free_count_finish)
            value_from_db = dbOperation.get_value(chat_id)
            
            #check operand
            if value_from_user['operand'] == '+':
                new_value = int(value_from_db) + int(value_from_user['value'])
            elif value_from_user['operand'] == '-':
                new_value = int(value_from_db) - int(value_from_user['value'])
            else:
                raise Exception("Не тот операнд - value_from_user['operand']")

            ### get group or private
            if message.chat.type == 'group':
                if message.chat.title is not None:
                    name = message.chat.title
                else:
                    name = ''
            elif message.chat.type == 'private':
                if message.chat.first_name is not None and message.chat.last_name is not None:
                    name = message.chat.first_name+' '+message.chat.last_name
                elif message.chat.first_name is not None:
                    name = message.chat.first_name
                elif message.chat.last_name is not None:
                    name = message.chat.last_name
                else:
                    name = ''
                if message.chat.username is not None:
                    name += ' @'+message.chat.username


            #set value
            send_value = dbOperation.set_value_db(new_value, name, chat_id)
            
            #send value
            send_value = '\U0001F911\U0001F911\U0001F911'+'\n'+str(send_value)
            bot.send_message(message.chat.id, send_value)

        #exceptions
        except exception_empty:
            pass
        except exception_message_clear as ex: 
            bot.send_message(message.chat.id, 'Ошибка: '+str(ex))
            #bot.send_message(message.chat.id, 'Ошибка: '+result)
        except exception_message as ex:
            bot.send_message(message.chat.id, 'Ошибка')
            write_log(str(ex))   
        except Exception as ex:
            bot.send_message(message.chat.id, 'Ошибка')
            write_log(str(exception_message.main(ex))) 

        finally:
            try:
                if 'dbOperation' in locals():
                    dbOperation.close()
            except Exception as ex:
                write_log(str(exception_message.main(ex))) 
 
    #bot.polling()
       
    print('Start bot')
    bot.polling(none_stop=True)
    print('Stop bot')
       
        
if __name__ == '__main__':
    telegram_bot(token)