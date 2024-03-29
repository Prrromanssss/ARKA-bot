import sqlite3

import settings


DB_TABLE = 'db_usernames'


class UserData:
    def __init__(self, name):
        self.name = name

    def db_insert(self, message, name):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        username = message.from_user.username
        val = (message.chat.id, username, name)
        sql_query = f'''SELECT
                           username
                        FROM {DB_TABLE}
                        WHERE user_id = ?
                     '''
        cursor.execute(sql_query, (message.chat.id,))
        if cursor.fetchall():
            sql_query = f'''UPDATE
                                {DB_TABLE}
                            SET user_name = ?
                            WHERE user_id = ?
                         '''
            cursor.execute(sql_query, (name, message.chat.id))
            conn.commit()
            return
        sql_query = f'''INSERT INTO
                            {DB_TABLE}
                        (user_id, "username", user_name)
                        VALUES (?, ?, ?)
                     '''
        cursor.execute(sql_query, val)
        conn.commit()

    def db_select_user(self, message):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        val = (message.chat.id, )
        sql_query = f'''SELECT
                            "user_name"
                        FROM {DB_TABLE}
                        WHERE user_id = ?
                     '''
        cursor.execute(sql_query, val)
        user_name = cursor.fetchall()[0][0]
        sql_query = f'''SELECT
                            "username"
                        FROM {DB_TABLE}
                        WHERE user_id = ?
                     '''
        cursor.execute(sql_query, val)
        username = cursor.fetchall()[0][0]
        conn.commit()
        return username, user_name

    def db_select_all_users_id(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        sql_query = f'''SELECT
                            "user_id"
                        FROM {DB_TABLE}
                     '''
        cursor.execute(sql_query)
        users_id = cursor.fetchall()
        conn.commit()
        return users_id


db_object = UserData(settings.DB_URI)
