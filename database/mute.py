import psycopg2
import time


class Database_mute:
    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table_mute()

    def create_table_mute(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users_mute (
                    id serial PRIMARY KEY,
                    user_id BIGINT UNIQUE,
                    mute_time INTEGER DEFAULT 0
                )
            """)

    def add_user(self, user_id):
        with self.conn:
            self.cur.execute("INSERT INTO users_mute (user_id) VALUES (%s)", (user_id,))
            self.conn.commit()

    def mute(self, user_id):
        with self.conn:
            user = self.cur.execute("SELECT * FROM users_mute WHERE user_id = %s", (user_id,)).fetchone()
            return int(user[2]) >= int(time.time())

    def add_mute(self, user_id, mute_time):
        with self.conn:
            self.cur.execute("""
                INSERT INTO users_mute (user_id, mute_time) VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET mute_time = EXCLUDED.mute_time
            """, (user_id, int(time.time()) + mute_time * 60))
            self.conn.commit()