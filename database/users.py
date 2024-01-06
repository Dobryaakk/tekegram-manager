import psycopg2
import datetime


class Database_user_all:
    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users_all (
                    user_id BIGINT PRIMARY KEY,
                    name TEXT,
                    time TIMESTAMP,
                    age TEXT DEFAULT 'не вказано',
                    sex TEXT DEFAULT 'не вказано'
                )
            """)

    def get_random_user_with_name_from_table(self):
        with self.conn:
            self.cur.execute(f"SELECT user_id, name, time FROM users_all ORDER BY RANDOM() LIMIT 1")
            result = self.cur.fetchone()
            if result:
                user_id, name, time = result
                return user_id, name, time
            else:
                return None, None, None

    def add_user_id(self, user_id, name):
        current_time = datetime.datetime.now()

        with self.conn:
            self.cur.execute("""
                INSERT INTO users_all (user_id, name, time)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            """, (user_id, name, current_time))


class Database_group:
    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_group (
                    id BIGINT PRIMARY KEY,
                    group_id BIGINT UNIQUE
                )
            """)

    def add_group_id(self, group_id):
        print(group_id)
        with self.conn:
            self.cur.execute("""
                INSERT INTO chat_group (group_id)
                VALUES (%s)
                ON CONFLICT (group_id) DO NOTHING
            """, (group_id,))
            self.conn.commit()

    def is_group_id_present(self, group_id):
        self.cur.execute("""
            SELECT * FROM chat_group WHERE group_id = %s""", (group_id,))
        rows = self.cur.fetchall()

        if not rows:
            return False
        else:
            return True

    def random_user_with_name_from_user_messages_table(self):
        with self.conn:
            self.cur.execute("SELECT user_id, name FROM user_messages ORDER BY RANDOM() LIMIT 1")
            result = self.cur.fetchone()
            if result:
                user_id, name = result
                return user_id, name
            else:
                return None, None

    def get_random_user_with_name_from_user_messages_table(self, current_user_id):
        with self.conn:
            self.cur.execute("SELECT user_id, name FROM user_messages WHERE user_id != %s ORDER BY RANDOM() LIMIT 1",
                             (current_user_id,))
            result = self.cur.fetchone()
            if result:
                user_id, name = result
                return user_id, name
            else:
                return None, None
