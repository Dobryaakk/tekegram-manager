import psycopg2


class MainWelRules:
    def __init__(self, host, user, password, db_name, table_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.table_name = table_name
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        group_id_wel BIGINT PRIMARY KEY,
                        text_welcome TEXT
                    )
                """)

    def add_welcome(self, group_id, text_welcome):
        with self.conn:
            self.cur.execute(f"""
                INSERT INTO {self.table_name} (group_id_wel, text_welcome) VALUES (%s, %s)
                ON CONFLICT (group_id_wel) DO UPDATE SET text_welcome = EXCLUDED.text_welcome;
            """, (group_id, text_welcome))

    def get_welcome(self, group_id):
        self.cur.execute(f"SELECT text_welcome FROM {self.table_name} WHERE group_id_wel = %s", (group_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return "Приветствие не установлено"

    def delete_rules(self, group_id):
        with self.conn:
            self.cur.execute(f"DELETE FROM {self.table_name} WHERE group_id_wel = %s", (group_id,))
            if self.cur.rowcount > 0:
                return True
            else:
                return False


class Database_welcome(MainWelRules):
    def __init__(self, host, user, password, db_name):
        super().__init__(host, user, password, db_name, "welcome")


class Database_rules(MainWelRules):
    def __init__(self, host, user, password, db_name):
        super().__init__(host, user, password, db_name, "rules")
