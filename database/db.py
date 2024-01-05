import datetime
import sqlite3
import time


class Database_group_iq:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                 CREATE TABLE IF NOT EXISTS iq (
                     user_id INTEGER,
                     group_id INTEGER,
                     name TEXT,
                     liters INTEGER,
                     last_command_time DATETIME,
                     PRIMARY KEY (user_id, group_id)
                 )
             """)

    def add_message(self, user_id, group_id, name, liters):
        now = datetime.datetime.now()
        last_command_time = now + datetime.timedelta(hours=12)
        with self.conn:
            self.cur.execute("""
                INSERT OR IGNORE INTO iq (user_id, group_id, name, liters, last_command_time)
                VALUES (?, ?, ?, 0, ?)
            """, (user_id, group_id, name, last_command_time))

            self.cur.execute("""
                UPDATE iq SET liters = liters + ? WHERE user_id = ? AND group_id = ?
            """, (liters, user_id, group_id))

            self.cur.execute("""
                UPDATE iq SET last_command_time = ? WHERE user_id = ? AND group_id = ?
            """, (last_command_time, user_id, group_id))

            self.conn.commit()

    def get_liters(self, user_id, group_id):
        with self.conn:
            self.cur.execute("""
                SELECT liters FROM iq WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            liters = self.cur.fetchone()
            if liters:
                return liters[0]
            else:
                return 0

    def remaining_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute("""
                SELECT last_command_time FROM iq WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time_str = result[0].split('.')[0]
                last_command_time = datetime.datetime.strptime(last_command_time_str, "%Y-%m-%d %H:%M:%S")
                time_difference = last_command_time - now
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                if hours > 0:
                    return f"{hours} ч. {minutes} мин."
                elif hours == 0 and minutes > 0:
                    return f"{minutes} мин. {seconds} сек."
                else:
                    return f"{seconds} сек."

    def check_message_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute("""
                SELECT last_command_time FROM iq WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time_str = result[0].split('.')[0]
                last_command_time = datetime.datetime.strptime(last_command_time_str, "%Y-%m-%d %H:%M:%S")
                return now > last_command_time
            else:
                return True

    def get_users_and_liters_in_group(self, group_id):
        with self.conn:
            self.cur.execute("""
                SELECT name, liters FROM iq WHERE group_id = ?
            """, (group_id,))
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data

    def get_all_users_and_liters(self):
        with self.conn:
            self.cur.execute("""
                SELECT name, liters FROM iq
            """)
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data


class Database_group_vodka:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                 CREATE TABLE IF NOT EXISTS vodka (
                     user_id INTEGER,
                     group_id INTEGER,
                     name TEXT,
                     liters INTEGER,
                     last_command_time DATETIME,
                     PRIMARY KEY (user_id, group_id)
                 )
             """)

    def add_message(self, user_id, group_id, name, liters):
        now = datetime.datetime.now()
        last_command_time = now + datetime.timedelta(hours=2)
        with self.conn:
            self.cur.execute("""
                INSERT OR IGNORE INTO vodka (user_id, group_id, name, liters, last_command_time)
                VALUES (?, ?, ?, 0, ?)
            """, (user_id, group_id, name, last_command_time))

            self.cur.execute("""
                UPDATE vodka SET liters = liters + ? WHERE user_id = ? AND group_id = ?
            """, (liters, user_id, group_id))

            self.cur.execute("""
                UPDATE vodka SET last_command_time = ? WHERE user_id = ? AND group_id = ?
            """, (last_command_time, user_id, group_id))

            self.conn.commit()

    def get_liters(self, user_id, group_id):
        with self.conn:
            self.cur.execute("""
                SELECT liters FROM vodka WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            liters = self.cur.fetchone()
            if liters:
                return liters[0]
            else:
                return 0

    def remaining_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute("""
                SELECT last_command_time FROM vodka WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time_str = result[0].split('.')[0]
                last_command_time = datetime.datetime.strptime(last_command_time_str, "%Y-%m-%d %H:%M:%S")
                time_difference = last_command_time - now
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                if hours > 0:
                    return f"{hours} ч. {minutes} мин."
                elif hours == 0 and minutes > 0:
                    return f"{minutes} мин. {seconds} сек."
                else:
                    return f"{seconds} сек."

    def check_message_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute("""
                SELECT last_command_time FROM vodka WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time_str = result[0].split('.')[0]
                last_command_time = datetime.datetime.strptime(last_command_time_str, "%Y-%m-%d %H:%M:%S")
                return now > last_command_time
            else:
                return True

    def get_users_and_liters_in_group(self, group_id):
        with self.conn:
            self.cur.execute("""
                SELECT name, liters FROM vodka WHERE group_id = ?
            """, (group_id,))
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data

    def get_all_users_and_liters(self):
        with self.conn:
            self.cur.execute("""
                SELECT name, liters FROM vodka
            """)
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data


class Database_group_beer:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                 CREATE TABLE IF NOT EXISTS beer (
                     user_id INTEGER,
                     group_id INTEGER,
                     name TEXT,
                     liters INTEGER,
                     last_command_time DATETIME,
                     PRIMARY KEY (user_id, group_id)
                 )
             """)

    def add_message(self, user_id, group_id, name, liters):
        now = datetime.datetime.now()
        last_command_time = now + datetime.timedelta(hours=1)
        with self.conn:
            self.cur.execute("""
                INSERT OR IGNORE INTO beer (user_id, group_id, name, liters, last_command_time)
                VALUES (?, ?, ?, 0, ?)
            """, (user_id, group_id, name, last_command_time))

            self.cur.execute("""
                UPDATE beer SET liters = liters + ? WHERE user_id = ? AND group_id = ?
            """, (liters, user_id, group_id))

            self.cur.execute("""
                UPDATE beer SET last_command_time = ? WHERE user_id = ? AND group_id = ?
            """, (last_command_time, user_id, group_id))

            self.conn.commit()

    def get_liters(self, user_id, group_id):
        with self.conn:
            self.cur.execute("""
                SELECT liters FROM beer WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            liters = self.cur.fetchone()
            if liters:
                return liters[0]
            else:
                return 0

    def remaining_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute("""
                SELECT last_command_time FROM beer WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time_str = result[0].split('.')[0]
                last_command_time = datetime.datetime.strptime(last_command_time_str, "%Y-%m-%d %H:%M:%S")
                time_difference = last_command_time - now
                minutes, seconds = divmod(time_difference.seconds, 60)
                if minutes <= 0:
                    return f"{seconds} сек."
                else:
                    return f"{minutes} мин. {seconds} ceк."

    def check_message_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute("""
                SELECT last_command_time FROM beer WHERE user_id = ? AND group_id = ?
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time_str = result[0].split('.')[0]
                last_command_time = datetime.datetime.strptime(last_command_time_str, "%Y-%m-%d %H:%M:%S")
                return now > last_command_time
            else:
                return True

    def get_users_and_liters_in_group(self, group_id):
        with self.conn:
            self.cur.execute("""
                SELECT name, liters FROM beer WHERE group_id = ?
            """, (group_id,))
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data

    def get_all_users_and_liters(self):
        with self.conn:
            self.cur.execute("""
                SELECT name, liters FROM beer
            """)
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data


class Database_user_all:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users_all (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    time INTEGER,
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
            self.cur.execute("INSERT OR IGNORE INTO users_all (user_id, name, time) VALUES (?, ?, ?)",
                             (user_id, name, current_time))


class Database_pred_user:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS pred (
                       user_id INTEGER,
                       name TEXT,
                       group_id INTEGER,
                       count_pred INTEGER, 
                       PRIMARY KEY (user_id, group_id)
                   )
               """)

    def add_or_update_user(self, user_id, name, group_id):
        with self.conn:
            self.cur.execute(
                "INSERT OR IGNORE INTO pred (user_id, name, group_id, count_pred) VALUES (?, ?, ?, 0)",
                (user_id, name, group_id))
            self.cur.execute(
                "UPDATE pred SET count_pred = count_pred + 1 WHERE user_id = ? AND name = ? AND group_id = ?",
                (user_id, name, group_id))

    def get_user_pred_count(self, user_id, group_id):
        with self.conn:
            self.cur.execute("SELECT count_pred FROM pred WHERE user_id = ? AND group_id = ?", (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                return result[0]
            else:
                return 0

    def get_group_messages_pred(self, group_id):
        with self.conn:
            self.cur.execute("SELECT user_id, name, count_pred FROM pred WHERE group_id = ?", (group_id,))
            group_messages = self.cur.fetchall()
            return group_messages

    def remove_user_entry(self, user_id, group_id):
        with self.conn:
            self.cur.execute("DELETE FROM pred WHERE user_id = ? AND group_id = ?", (user_id, group_id))


class Database_pred_dead:
    '''DATABASE_LANGUAGE'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS pred_dead (
                group_id INTEGER,
                dead TEXT DEFAULT 'bun'
            )
            """)

    def insert_or_update_data_dead(self, group_id, dead_value):
        with self.conn:
            self.cur.execute("""
            SELECT group_id FROM pred_dead WHERE group_id = ?
            """, (group_id,))
            existing_group = self.cur.fetchone()

            if existing_group:
                self.cur.execute("""
                UPDATE pred_dead SET dead = ? WHERE group_id = ?
                """, (dead_value, group_id))
            else:
                self.cur.execute("""
                INSERT INTO pred_dead (group_id, dead)
                VALUES (?, ?)
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
    '''DATABASE_LANGUAGE'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS pred_table (
                group_id INTEGER,
                pred INTEGER DEFAULT 3
            )
            """)

    def insert_or_update_data(self, group_id, pred_value):
        with self.conn:
            self.cur.execute("""
            SELECT group_id FROM pred_table WHERE group_id = ?
            """, (group_id,))
            existing_group = self.cur.fetchone()

            if existing_group:
                self.cur.execute("""
                UPDATE pred_table SET pred = ? WHERE group_id = ?
                """, (pred_value, group_id))
            else:
                self.cur.execute("""
                INSERT INTO pred_table (group_id, pred)
                VALUES (?, ?)
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


class Database_language:
    '''DATABASE_LANGUAGE'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS language (
                       user_id INTEGER,
                       lang TEXT
                       )
               """)

    def add_user_lang(self, user_id, lang):
        with self.conn:
            self.cur.execute("INSERT INTO language VALUES (?, ?)", (user_id, lang))


class Database_group_bad_words:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS bad_message (
                       user_id INTEGER,
                       name TEXT,
                       group_id INTEGER,
                       message_count INTEGER,
                       PRIMARY KEY (user_id, group_id)
                   )
               """)

    def add_or_update_user(self, user_id, name, group_id):
        with self.conn:
            self.cur.execute(
                "INSERT OR IGNORE INTO bad_message (user_id, name, group_id, message_count) VALUES (?, ?, ?, 0)",
                (user_id, name, group_id))
            self.cur.execute(
                "UPDATE bad_message SET message_count = message_count + 1 WHERE user_id = ? AND name = ? AND group_id = ?",
                (user_id, name, group_id))

    def get_group_messages(self, group_id):
        with self.conn:
            self.cur.execute("SELECT user_id, name, message_count FROM bad_message WHERE group_id = ?", (group_id,))
            group_messages = self.cur.fetchall()
            return group_messages

    def get_total_message_count_for_group(self, group_id):
        with self.conn:
            self.cur.execute("SELECT SUM(message_count) FROM bad_message WHERE group_id = ?", (group_id,))
            total_message_count = self.cur.fetchone()[0]
            return total_message_count


class Database_group_bad_words_day:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()
        self.delete_old_records()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS bad_message_day (
                       user_id INTEGER,
                       name TEXT,
                       group_id INTEGER,
                       message_time DATETIME,
                       message_count INTEGER,
                       PRIMARY KEY (user_id, group_id, message_time)
                   )
               """)

    def add_new_message(self, user_id, name, group_id):
        current_time = datetime.datetime.now()

        with self.conn:
            self.cur.execute(
                "INSERT INTO bad_message_day (user_id, name, group_id, message_time, message_count) VALUES (?, ?, ?, ?, 1)",
                (user_id, name, group_id, current_time))

    def delete_old_records(self):
        cutoff_time = datetime.datetime.now() - datetime.timedelta(weeks=4)
        with self.conn:
            self.cur.execute("DELETE FROM bad_message_day WHERE message_time < ?", (cutoff_time,))

    def get_top_messages_last_24_hours(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(hours=24)

        with self.conn:
            self.cur.execute("""
                SELECT user_id, name, SUM(message_count) as total_messages
                FROM bad_message_day
                WHERE group_id = ? AND message_time >= ?
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
                WHERE group_id = ? AND message_time >= ?
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
                  WHERE group_id = ? AND message_time >= ?
                  GROUP BY user_id, name
                  ORDER BY total_messages DESC
              """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages

    def get_total_message_count_for_group(self, group_id):
        with self.conn:
            self.cur.execute("SELECT SUM(message_count) FROM bad_message_day WHERE group_id = ?", (group_id,))
            total_message_count = self.cur.fetchone()[0]
            return total_message_count


class Database_group_words:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS user_messages (
                       user_id INTEGER,
                       name TEXT,
                       group_id INTEGER,
                       message_count INTEGER,
                       PRIMARY KEY (user_id, group_id)
                   )
               """)

    def add_or_update_user(self, user_id, name, group_id):
        with self.conn:
            self.cur.execute(
                "INSERT OR IGNORE INTO user_messages (user_id, name, group_id, message_count) VALUES (?, ?, ?, 0)",
                (user_id, name, group_id))
            self.cur.execute(
                "UPDATE user_messages SET message_count = message_count + 1 WHERE user_id = ? AND name = ? AND group_id = ?",
                (user_id, name, group_id))

    def get_group_messages(self, group_id):
        with self.conn:
            self.cur.execute("SELECT user_id, name, message_count FROM user_messages WHERE group_id = ?", (group_id,))
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
            self.cur.execute("SELECT SUM(message_count) FROM user_messages WHERE group_id = ?", (group_id,))
            total_message_count = self.cur.fetchone()[0]
            return total_message_count


class Database_group_words_day:
    '''MESSAGE GROUP'''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()
        self.delete_old_records()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS messages_day (
                       user_id INTEGER,
                       name TEXT,
                       group_id INTEGER,
                       message_time DATETIME,
                       message_count INTEGER,
                       PRIMARY KEY (user_id, group_id, message_time)
                   )
               """)

    def add_new_message(self, user_id, name, group_id):
        current_time = datetime.datetime.now()

        with self.conn:
            self.cur.execute(
                "INSERT INTO messages_day (user_id, name, group_id, message_time, message_count) VALUES (?, ?, ?, ?, 1)",
                (user_id, name, group_id, current_time))

    def delete_old_records(self):
        cutoff_time = datetime.datetime.now() - datetime.timedelta(weeks=4)
        with self.conn:
            self.cur.execute("DELETE FROM messages_day WHERE message_time < ?", (cutoff_time,))

    def get_top_messages_last_24_hours(self, group_id):
        current_time = datetime.datetime.now()

        cutoff_time = current_time - datetime.timedelta(hours=24)

        with self.conn:
            self.cur.execute("""
                SELECT user_id, name, SUM(message_count) as total_messages
                FROM messages_day
                WHERE group_id = ? AND message_time >= ?
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
                WHERE group_id = ? AND message_time >= ?
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
                  WHERE group_id = ? AND message_time >= ?
                  GROUP BY user_id, name
                  ORDER BY total_messages DESC
              """, (group_id, cutoff_time))

            top_messages = self.cur.fetchall()

        return top_messages


class Database_group:
    '''
    GROUP
    '''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_group_id()

    def create_group_id(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_group (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER UNIQUE
                )
            """)

    def add_group_id(self, group_id):
        with self.conn:
            self.cur.execute("""
            INSERT OR IGNORE INTO chat_group (group_id) VALUES (?)""", (group_id,))
            self.conn.commit()

    def is_group_id_present(self, group_id):
        self.cur.execute("""
            SELECT * FROM chat_group WHERE group_id = ?""", (group_id,))
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
            self.cur.execute("SELECT user_id, name FROM user_messages WHERE user_id != ? ORDER BY RANDOM() LIMIT 1",
                             (current_user_id,))
            result = self.cur.fetchone()
            if result:
                user_id, name = result
                return user_id, name
            else:
                return None, None


class Database_rules:
    '''
    RULES
    '''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_rules()

    def create_rules(self):
        with self.conn:
            self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS rules (
                        group_id INTEGER PRIMARY KEY,
                        text_rules TEXT
                    )
                """)

    def add_rules(self, group_id, text_rules):
        with self.conn:
            self.cur.execute("INSERT OR REPLACE INTO rules (group_id, text_rules) VALUES (?, ?)",
                             (group_id, text_rules))

    def get_rules(self, group_id):
        self.cur.execute("SELECT text_rules FROM rules WHERE group_id = ?", (group_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return 'Правила не установлены'

    def delete_rules(self, group_id):
        with self.conn:
            self.cur.execute("DELETE FROM rules WHERE group_id = ?", (group_id,))
            if self.cur.rowcount > 0:
                return True
            else:
                return False


class Database_mute:
    '''
    MUTE
    '''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table_mute()

    def create_table_mute(self):
        with self.conn:
            self.cur.execute("""
                  CREATE TABLE IF NOT EXISTS users_mute (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER UNIQUE,
                      mute_time INTEGER DEFAULT 0
                  )
              """)

    def add_user(self, user_id):
        with self.conn:
            self.cur.execute("INSERT INTO users_mute (user_id) VALUES (?)", (user_id,))
            self.conn.commit()

    def mute(self, user_id):
        with self.conn:
            user = self.cur.execute("SELECT * FROM users_mute WHERE user_id = ?", (user_id,)).fetchone()
            return int(user[2]) >= int(time.time())

    def add_mute(self, user_id, mute_time):
        with self.conn:
            self.cur.execute("INSERT OR REPLACE INTO users_mute (user_id, mute_time) VALUES (?, ?)",
                             (user_id, int(time.time()) + mute_time * 60))
            self.conn.commit()


class Database_add_admin:
    '''
    ADD_ADMIN
    '''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.user_admin()

    def user_admin(self):
        with self.conn:
            self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS user_admin (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER UNIQUE,
                            name TEXT
                        )
                    """)

    def user_admin_exists(self, user_id):
        with self.conn:
            result = self.cur.execute("SELECT * FROM user_admin WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_admin_user(self, user_id, full_name):
        if not self.user_admin_exists(user_id):
            with self.conn:
                self.cur.execute("INSERT INTO user_admin (user_id, name) VALUES (?, ?)", (user_id, full_name,))
                self.conn.commit()

    def staff(self):
        with self.conn:
            res_adm = self.cur.execute("SELECT name FROM user_admin").fetchall()
            return [name[0] for name in res_adm]

    def is_admin(self, user_id_or_username):
        with self.conn:
            result = self.cur.execute("SELECT * FROM user_admin WHERE user_id = ? OR name = ?",
                                      (user_id_or_username, user_id_or_username)).fetchall()
            return bool(len(result))

    def remove_admin(self, user_id_or_username):
        with self.conn:
            self.cur.execute("DELETE FROM user_admin WHERE user_id = ? OR name = ?",
                             (user_id_or_username, user_id_or_username))
            self.conn.commit()


class Database_welcome:
    '''
    WELCOME
    '''

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.welcome()

    def welcome(self):
        with self.conn:
            self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS welcome (
                        group_id_wel INTEGER PRIMARY KEY,
                        text_welcome TEXT
                    )
                """)

    def add_welcome(self, group_id, text_welcome):
        with self.conn:
            self.cur.execute("INSERT OR REPLACE INTO welcome (group_id_wel, text_welcome) VALUES (?, ?)",
                             (group_id, text_welcome))

    def get_welcome(self, group_id):
        self.cur.execute("SELECT text_welcome FROM welcome WHERE group_id_wel = ?", (group_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return "Приветствие не установлено"
