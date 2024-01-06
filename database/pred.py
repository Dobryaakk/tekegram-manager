import psycopg2


class Database_pred_user:
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
                   CREATE TABLE IF NOT EXISTS pred (
                       user_id BIGINT,
                       name TEXT,
                       group_id BIGINT,
                       count_pred INTEGER, 
                       PRIMARY KEY (user_id, group_id)
                   )
               """)

    def add_or_update_user(self, user_id, name, group_id):
        with self.conn:
            self.cur.execute("""
                INSERT INTO pred (user_id, name, group_id, count_pred) 
                VALUES (%s, %s, %s, 1) 
                ON CONFLICT (user_id, group_id) DO UPDATE SET count_pred = pred.count_pred + 1
            """, (user_id, name, group_id))

    def get_user_pred_count(self, user_id, group_id):
        with self.conn:
            self.cur.execute("SELECT count_pred FROM pred WHERE user_id = %s AND group_id = %s", (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                return result[0]
            else:
                return 0

    def get_group_messages_pred(self, group_id):
        with self.conn:
            self.cur.execute("SELECT user_id, name, count_pred FROM pred WHERE group_id = %s", (group_id,))
            group_messages = self.cur.fetchall()
            return group_messages

    def remove_user_entry(self, user_id, group_id):
        with self.conn:
            self.cur.execute("DELETE FROM pred WHERE user_id = %s AND group_id = %s", (user_id, group_id))


class Database_pred_dead:
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
            CREATE TABLE IF NOT EXISTS pred_dead (
                group_id BIGINT,
                dead TEXT DEFAULT 'bun'
            )
            """)

    def insert_or_update_data_dead(self, group_id, dead_value):
        with self.conn:
            self.cur.execute("""
            SELECT group_id FROM pred_dead WHERE group_id = %s
            """, (group_id,))
            existing_group = self.cur.fetchone()

            if existing_group:
                self.cur.execute("""
                UPDATE pred_dead SET dead = %s WHERE group_id = %s
                """, (dead_value, group_id))
            else:
                self.cur.execute("""
                INSERT INTO pred_dead (group_id, dead)
                VALUES (%s, %s)
                """, (group_id, dead_value))

    def get_default_dead_text(self):
        with self.conn:
            self.cur.execute("""
               SELECT dead FROM pred_dead LIMIT 1
               """)
            row = self.cur.fetchone()
            if row:
                return row[0]
            else:
                return 'bun'


class Database_pred:
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
            CREATE TABLE IF NOT EXISTS pred_table (
                group_id BIGINT,
                pred INTEGER DEFAULT 3
            )
            """)

    def insert_or_update_data(self, group_id, pred_value):
        with self.conn:
            self.cur.execute("""
            SELECT group_id FROM pred_table WHERE group_id = %s
            """, (group_id,))
            existing_group = self.cur.fetchone()

            if existing_group:
                self.cur.execute("""
                UPDATE pred_table SET pred = %s WHERE group_id = %s
                """, (pred_value, group_id))
            else:
                self.cur.execute("""
                INSERT INTO pred_table (group_id, pred)
                VALUES (%s, %s)
                """, (group_id, pred_value))

    def get_default_pred_value(self):
        with self.conn:
            self.cur.execute("""
            SELECT pred FROM pred_table LIMIT 1
            """)
            row = self.cur.fetchone()
            if row:
                return row[0]
            else:
                return 3
