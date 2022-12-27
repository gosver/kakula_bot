import pymysql

from my_modules.exception_message import exception_message

#db connect, operate
class dbOperations():
  
    #init
    def __init__(self, db):
      self.db = db
       
    #connect 
    def connect(self):  
        try:
            db=self.db
            self.connection = pymysql.connect(
                host=db['host'],
                port=3306,
                user=db['user'],
                password=db['password'],
                database=db['dbname'],
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as ex:
            raise exception_message(exception_message.main(ex,self))
      
    #check existing tables, rows
    def check_tables(self):
        
        try:
            #create table
            with self.connection.cursor() as cursor:
                create_table_query = "CREATE TABLE IF NOT EXISTS `value`(id int AUTO_INCREMENT,"\
                                     " chat_id varchar(32),"\
                                     " value varchar(32), PRIMARY KEY (id));"
                cursor.execute(create_table_query)
            
            #find str №1
            '''with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(1) FROM `value` WHERE id=1")
                version = cursor.fetchone()

                if version['COUNT(1)'] == 0:
                    #json_user_ids = json.dumps('{ "0": "414847524", "1" : "414847521"}')
                    #insert_table_query = f'INSERT INTO `value` (id,value,usr_ids) VALUES (1,0,{json_user_ids});'
                    insert_table_query = f'INSERT INTO `value` (id,value) VALUES (1,0);'
                    cursor.execute(insert_table_query)
                    self.connection.commit()'''
        
        except Exception as ex:
            raise exception_message(exception_message.main(ex,self))
           
    #check existing tables, rows
    def select_chatid(self, chat_id):
        
        try:
            #select
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `value` WHERE `chat_id` = {chat_id};")
                version = cursor.fetchone()

                #check existence entry and add entry
                if version == None:
                    cursor.execute(f"INSERT INTO `value` (chat_id, value) values({chat_id}, 0);")     

        except Exception as ex:
            raise exception_message(exception_message.main(ex,self))
                  
              
    #get value db
    def get_value(self, chat_id):

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT value FROM `value` WHERE chat_id={chat_id}")
                version = cursor.fetchone()
                return version['value']

        except Exception as ex:
            raise exception_message(exception_message.main(ex,self))

    #set value db       
    def set_value_db(self, value, chat_id):

        #find data
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE `value` SET `value` = '{value}' WHERE `value`.`chat_id` = {chat_id};")
                self.connection.commit()
                return value

        except Exception as ex:
            raise exception_message(exception_message.main(ex,self))
       
    #close db connection     
    def close(self):
        try:
            if hasattr(self,'connection'):
                self.connection.close()
        except Exception as ex:
            raise exception_message(exception_message.main(ex,self))