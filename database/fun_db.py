import datetime
import psycopg2


class MainFun:
    def __init__(self, host, user, password, db_name, table_name, command_hours):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.table_name = table_name
        self.command_hours = command_hours
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    user_id BIGINT PRIMARY KEY,
                    group_id BIGINT,
                    name TEXT,
                    liters REAL,
                    last_command_time TIMESTAMP,
                    UNIQUE(user_id, group_id)
                )
            """)

    def add_message(self, user_id, group_id, name, liters):
        now = datetime.datetime.now()
        last_command_time = now + datetime.timedelta(hours=self.command_hours)
        with self.conn:
            self.cur.execute(f"""
                INSERT INTO {self.table_name} (user_id, group_id, name, liters, last_command_time)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET group_id = EXCLUDED.group_id,
                    name = EXCLUDED.name,
                    liters = {self.table_name}.liters + EXCLUDED.liters,
                    last_command_time = EXCLUDED.last_command_time
            """, (user_id, group_id, name, liters, last_command_time))

            self.conn.commit()

    def get_liters(self, user_id, group_id):
        with self.conn:
            self.cur.execute(f"""
                SELECT liters FROM {self.table_name} WHERE user_id = %s AND group_id = %s
            """, (user_id, group_id))
            liters = self.cur.fetchone()
            if liters:
                return liters[0]
            else:
                return 0

    def remaining_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute(f"""
                SELECT last_command_time FROM {self.table_name} WHERE user_id = %s AND group_id = %s
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time = result[0]
                time_difference = last_command_time - now
                minutes, seconds = divmod(time_difference.seconds, 60)
                hours, minutes = divmod(minutes, 60)

                time_parts = []

                if hours > 0:
                    time_parts.append(f"{hours} год.")

                if minutes > 0 or (hours == 0 and seconds > 0):
                    time_parts.append(f"{minutes} мин.")

                if seconds > 0:
                    time_parts.append(f"{seconds} сек.")

                return " ".join(time_parts) if time_parts else "менше секунди"
        return "невідомий час"

    def check_message_time(self, user_id, group_id):
        now = datetime.datetime.now()
        with self.conn:
            self.cur.execute(f"""
                SELECT last_command_time FROM {self.table_name} WHERE user_id = %s AND group_id = %s
            """, (user_id, group_id))
            result = self.cur.fetchone()
            if result:
                last_command_time = result[0]
                return now > last_command_time
            else:
                return True

    def get_users_and_liters_in_group(self, group_id):
        with self.conn:
            self.cur.execute(f"""
                SELECT name, liters FROM {self.table_name} WHERE group_id = %s
            """, (group_id,))
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data

    def get_all_users_and_liters(self):
        with self.conn:
            self.cur.execute(f"""
                SELECT name, liters FROM {self.table_name}
            """)
            results = self.cur.fetchall()
            user_data = [(name, liters) for name, liters in results]
            return user_data


class Database_group_iq(MainFun):
    def __init__(self, host, user, password, db_name):
        super().__init__(host, user, password, db_name, "iq", 12)


class Database_group_vodka(MainFun):
    def __init__(self, host, user, password, db_name):
        super().__init__(host, user, password, db_name, "vodka", 2)


class Database_group_beer(MainFun):
    def __init__(self, host, user, password, db_name):
        super().__init__(host, user, password, db_name, "beer", 1)
