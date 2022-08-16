import psycopg2
import config


class UserData:
    def __init__(self, name):
        self.name = name

    def db_insert(self, message, name):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        username = message.from_user.username
        val = (message.chat.id, username, name)
        sql_query = f'SELECT username FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        if cursor.fetchall():
            return
        sql_query = f'INSERT INTO {config.DB_TABLE} ("user_id", "username", "user_name") VALUES (%s, %s, %s)'
        cursor.execute(sql_query, val)
        conn.commit()

    def db_select_user(self, message):

        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        val = (message.chat.id, )
        sql_query = f'SELECT ("username", "user_name") FROM {config.DB_TABLE} WHERE user_id = %s'
        cursor.execute(sql_query, val)
        username = cursor.fetchall()[0]
        conn.commit()
        return username

    def db_select_all_users_id(self):
        conn = psycopg2.connect(self.name, sslmode='require')
        cursor = conn.cursor()
        sql_query = f'SELECT "user_id" FROM {config.DB_TABLE}'
        cursor.execute(sql_query)
        users_id = cursor.fetchall()
        conn.commit()
        return users_id


db_object = UserData(config.DB_URI)