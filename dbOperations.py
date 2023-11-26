import datetime

import pymysql

from my_modules.exception_message import exception_message, exception_message_clear

table_calcualtions_name = 'calculations'
table_free_counts = 'free_calculations'
count_free_calcualtions = 100
text_free_counts_limmit = '''Доброго времени суток)
Вы использовали бесплатный лимит операций.
Для дальнейшей работы бота, нужно оплатить его подписку на год. 
Почему не бесплатно?:
 ⁃ бот живет на сервере, за который нужно платить
 ⁃ как и любая техника, бот требует обслуживание для бесперебойной работы
Стоимость подписки на один год 60$.
Для оплаты перейдите свяжитесь с администратором @vitalii_naletov'''
text_license_limmit = '''Доброго времени суток) 
Закончилась годовая подписка. 
Стоимость подписки на один год 60$.
Для оплаты перейдите свяжитесь с администратором @vitalii_naletov'''

# db connect, operate
class dbOperations():
    tries = 3

    # init
    def __init__(self, db):
        self.db = db

    # connect
    def connect(self):
        try:
            db = self.db
            self.connection = pymysql.connect(
                host=db['host'],
                port=3306,
                user=db['user'],
                password=db['password'],
                database=db['dbname'],
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as ex:
            raise exception_message(exception_message.main(ex, self))

    # check existing tables, rows
    def check_tables(self):

        try:
            # create table
            with self.connection.cursor() as cursor:
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_calcualtions_name} (id int AUTO_INCREMENT," \
                                     " chat_id varchar(32) UNIQUE," \
                                     " value varchar(32), "\
                                     " date_start DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                                     " active_license BOOLEAN NOT NULL DEFAULT 0," \
                                     "PRIMARY KEY(id));"

                create_table_query2 = f" CREATE TABLE IF NOT EXISTS {table_free_counts} ( " \
                "id int, " \
                "free_counts int(5) " \
                ",constraint wt_pk primary key(id)" \
                f",constraint wt_fk foreign key(id) REFERENCES {table_calcualtions_name}(id));"

                cursor.execute(create_table_query)
                cursor.execute(create_table_query2)



        except Exception as ex:
            raise exception_message(exception_message.main(ex, self))

    # check existing tables, rows
    def select_chatid(self, chat_id):

        try:
            # select
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_calcualtions_name}  WHERE `chat_id` = {chat_id};")
                version = cursor.fetchone()

                # check existence entry and add entry
                if version == None:
                    cursor.execute(f"INSERT INTO {table_calcualtions_name}  (chat_id, value) values({chat_id}, 0);")
                    id = cursor.lastrowid
                    cursor.execute(f"INSERT INTO {table_free_counts}  (id, free_counts) values({id}, {count_free_calcualtions});")

        except Exception as ex:
            raise exception_message(exception_message.main(ex, self))

    # get value db
    def get_value(self, chat_id):

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT value FROM {table_calcualtions_name}  WHERE chat_id={chat_id}")
                version = cursor.fetchone()
                return version['value']

        except Exception as ex:
            raise exception_message(exception_message.main(ex, self))

    # set value db
    def set_value_db(self, value, name, chat_id):

        # find data
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE {table_calcualtions_name}  SET `value` = '{value}', `name` = '{name}' WHERE {table_calcualtions_name} .`chat_id` = {chat_id};")
                self.connection.commit()
                return value

        except Exception as ex:
            raise exception_message(exception_message.main(ex, self))

    # close db connection
    def close(self):
        try:
            if hasattr(self, 'connection'):
                self.connection.close()
        except Exception as ex:
            raise exception_message(exception_message.main(ex, self))

    def get_active_status(self, chat_id):
        try:
            with self.connection.cursor() as cursor:
                query = f"SELECT {table_free_counts}.id ,active_license, free_counts, date_end FROM {table_calcualtions_name} "\
                      f"INNER JOIN {table_free_counts} ON {table_calcualtions_name}.id={table_free_counts}.id " \
                      f"WHERE {table_calcualtions_name}.chat_id={chat_id};"
                cursor.execute(query)
                chat_entity = cursor.fetchone()
                if not chat_entity['active_license']:
                    if chat_entity['free_counts'] > 0:
                        current_count = chat_entity['free_counts'] - 1
                        cursor.execute(f"UPDATE {table_free_counts}  SET `free_counts` = '{current_count}' WHERE `id` = {chat_entity['id']};")
                    else:
                        return (text_free_counts_limmit)
                else:
                    date_end = chat_entity['date_end']
                    delta = date_end - datetime.datetime.now()
                    delta_seconds = delta.total_seconds()
                    if delta_seconds < 0:
                        return text_license_limmit

        except TypeError as ex:
            if self.tries <= 0 or ex.args[0] != "'NoneType' object is not subscriptable":
                raise exception_message(exception_message.main(ex, self))
            else:
                try:
                    self.tries -= 1
                    with self.connection.cursor() as cursor:
                        query = f"INSERT INTO `{table_free_counts}`(id, free_counts)" \
                            f"SELECT id , {count_free_calcualtions} FROM {table_calcualtions_name} c WHERE c.chat_id={chat_id}"
                        cursor.execute(query)
                        self.get_active_status(chat_id)
                except Exception as ex:
                    raise exception_message(exception_message.main(ex, self))
        except Exception as ex:
            raise exception_message(exception_message.main(ex, self))

