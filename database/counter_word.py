import datetime
import psycopg2


class Database_group_bad_words:
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
                CREATE TABLE IF NOT EXISTS bad_message (
                    user_id BIGINT,
                    name TEXT,
                    group_id BIGINT,
                    message_count INTEGER,
                    PRIMARY KEY (user_id, group_id),
                    UNIQUE (user_id, group_id)
                )
            """)

    def add_or_update_user(self, user_id, name, group_id):
        with self.conn:
            self.cur.execute(
                "INSERT INTO bad_message (user_id, name, group_id, message_count) VALUES (%s, %s, %s, 0) "
                "ON CONFLICT (user_id, group_id) DO NOTHING",
                (user_id, name, group_id)
            )
            self.cur.execute(
                "UPDATE bad_message SET message_count = message_count + 1 "
                "WHERE user_id = %s AND group_id = %s",
                (user_id, group_id)
            )

    def get_group_messages(self, group_id):
        with self.conn:
            self.cur.execute("SELECT user_id, name, message_count FROM bad_message WHERE group_id = %s", (group_id,))
            group_messages = self.cur.fetchall()
            return group_messages

    def get_total_message_count_for_group(self, group_id):
        with self.conn:
            self.cur.execute("SELECT SUM(message_count) FROM bad_message WHERE group_id = %s", (group_id,))
            total_message_count = self.cur.fetchone()[0]
            return total_message_count


class Database_group_bad_words_day:
    '''MESSAGE GROUP'''

    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table()
        self.delete_old_records()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS bad_message_day (
                    user_id BIGINT,
                    name TEXT,
                    group_id BIGINT,
                    message_time TIMESTAMP,
                    message_count INTEGER,
                    PRIMARY KEY (user_id, group_id, message_time)
                )
            """)

    def add_new_message(self, user_id, name, group_id):
        current_time = datetime.datetime.now()

        with self.conn:
            self.cur.execute(
                "INSERT INTO bad_message_day (user_id, name, group_id, message_time, message_count) "
                "VALUES (%s, %s, %s, %s, 1)",
                (user_id, name, group_id, current_time)
            )

    def delete_old_records(self):
        cutoff_time = datetime.datetime.now() - datetime.timedelta(weeks=4)
        with self.conn:
            self.cur.execute("DELETE FROM bad_message_day WHERE message_time < %s", (cutoff_time,))

    def get_top_messages_last_24_hours(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(hours=24)

        with self.conn:
            self.cur.execute("""
                SELECT user_id, name, SUM(message_count) as total_messages
                FROM bad_message_day
                WHERE group_id = %s AND message_time >= %s
                GROUP BY user_id, name
                ORDER BY total_messages DESC
            """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages

    def get_top_messages_last_week(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(weeks=1)

        with self.conn:
            self.cur.execute("""
                SELECT user_id, name, SUM(message_count) as total_messages
                FROM bad_message_day
                WHERE group_id = %s AND message_time >= %s
                GROUP BY user_id, name
                ORDER BY total_messages DESC
            """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages

    def get_top_messages_last_month(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(weeks=4)

        with self.conn:
            self.cur.execute("""
                  SELECT user_id, name, SUM(message_count) as total_messages
                  FROM bad_message_day
                  WHERE group_id = %s AND message_time >= %s
                  GROUP BY user_id, name
                  ORDER BY total_messages DESC
              """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages

    def get_total_message_count_for_group(self, group_id):
        with self.conn:
            self.cur.execute("SELECT SUM(message_count) FROM bad_message_day WHERE group_id = %s", (group_id,))
            total_message_count = self.cur.fetchone()[0]
            return total_message_count


class Database_group_words:
    '''MESSAGE GROUP'''

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
                CREATE TABLE IF NOT EXISTS user_messages (
                    user_id BIGINT,
                    name TEXT,
                    group_id BIGINT,
                    message_count INTEGER,
                    PRIMARY KEY (user_id, group_id),
                    UNIQUE (user_id, group_id)
                )
            """)

    def add_or_update_user(self, user_id, name, group_id):
        with self.conn:
            self.cur.execute(
                "INSERT INTO user_messages (user_id, name, group_id, message_count) VALUES (%s, %s, %s, 0) "
                "ON CONFLICT (user_id, group_id) DO NOTHING",
                (user_id, name, group_id)
            )
            self.cur.execute(
                "UPDATE user_messages SET message_count = message_count + 1 "
                "WHERE user_id = %s AND group_id = %s",
                (user_id, group_id)
            )

    def get_group_messages(self, group_id):
        with self.conn:
            self.cur.execute("SELECT user_id, name, message_count FROM user_messages WHERE group_id = %s", (group_id,))
            group_messages = self.cur.fetchall()
            return group_messages

    def get_random_user_with_name_from_user_messages_table(self):
        with self.conn:
            self.cur.execute("SELECT user_id, name FROM user_messages ORDER BY RANDOM() LIMIT 1")
            result = self.cur.fetchone()
            if result:
                user_id, name = result
                return user_id, name
            else:
                return None, None

    def get_total_message_count_for_group(self, group_id):
        with self.conn:
            self.cur.execute("SELECT SUM(message_count) FROM user_messages WHERE group_id = %s", (group_id,))
            total_message_count = self.cur.fetchone()[0]
            return total_message_count


class Database_group_words_day:
    '''MESSAGE GROUP'''

    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table()
        self.delete_old_records()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS messages_day (
                    user_id BIGINT,
                    name TEXT,
                    group_id BIGINT,
                    message_time TIMESTAMP,
                    message_count INTEGER,
                    PRIMARY KEY (user_id, group_id, message_time)
                )
            """)

    def add_new_message(self, user_id, name, group_id):
        current_time = datetime.datetime.now()

        with self.conn:
            self.cur.execute(
                "INSERT INTO messages_day"
                " (user_id, name, group_id, message_time, message_count) VALUES (%s, %s, %s, %s, 1)",
                (user_id, name, group_id, current_time))

    def delete_old_records(self):
        cutoff_time = datetime.datetime.now() - datetime.timedelta(weeks=4)
        with self.conn:
            self.cur.execute("DELETE FROM messages_day WHERE message_time < %s", (cutoff_time,))

    def get_top_messages_last_24_hours(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(hours=24)

        with self.conn:
            self.cur.execute("""
                SELECT user_id, name, SUM(message_count) as total_messages
                FROM messages_day
                WHERE group_id = %s AND message_time >= %s
                GROUP BY user_id, name
                ORDER BY total_messages DESC
            """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages

    def get_top_messages_last_week(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(weeks=1)

        with self.conn:
            self.cur.execute("""
                SELECT user_id, name, SUM(message_count) as total_messages
                FROM messages_day
                WHERE group_id = %s AND message_time >= %s
                GROUP BY user_id, name
                ORDER BY total_messages DESC
            """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages

    def get_top_messages_last_month(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(weeks=4)

        with self.conn:
            self.cur.execute("""
                  SELECT user_id, name, SUM(message_count) as total_messages
                  FROM messages_day
                  WHERE group_id = %s AND message_time >= %s
                  GROUP BY user_id, name
                  ORDER BY total_messages DESC
              """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages

