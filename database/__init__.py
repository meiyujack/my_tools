import sqlite3


class Database:

    def __init__(self, server, **kwargs):
        """
        Initialize basic information about current database.
        @param server: database name, like mariadb, sqlite, etc.
        @param kwargs: key=value. if sqlite, file_address, and sql_address in case want to reconstruct table;
        if mariadb, host={host}, user={user}, etc.
        """
        self.server = server
        self.basic = kwargs
        self.conn = None

    def connect_db(self):
        """
        Connect to the database.
        """
        try:
            if self.server == sqlite3:
                self.conn = self.server.connect(self.basic['file_address'])
            else:
                self.conn = self.server.connect(
                    user=self.basic['user'],
                    password=self.basic['password'],
                    host=self.basic['host'],
                    port=self.basic['port'],
                    database=self.basic['database'])
        except self.server.Error as e:
            return e

    def init_table(self):
        """
        Initialize table schema structure.
        """
        with open(self.basic["sql_address"], mode="r") as file:
            self.conn.cursor().executescript(file.read())
            self.conn.commit()
            print("Initialize database completed.")

    def select_db(self, table, get='*', prep=None, **condition):
        """
        Just execute "select" sentence.
        @param table: str, table's name.
        @param get: str, default: *, what column or property you want to get.
        @param prep: str, default:None, prep. "and" or "or(secondly)" in WHERE clause. At most two conditions now.
        @param condition: **condition, according to what condition you want to find.
        @return: rows if execute select sentence or error message.
        """
        sql = f"SELECT {get} FROM {table}"
        try:
            if condition:
                where = f" WHERE {','.join(condition.keys())}={','.join(['?'])}" if self.server == sqlite3 else f" WHERE {','.join(condition.keys())}={','.join(['%s'])}"
                if len(condition) == 1:
                    sql += where
                else:
                    where = f' {prep} '.join([
                        f"{''.join(m.keys())}={''.join(['?'])}" for m in [{
                            i: j
                        } for i, j in condition.items()]
                    ])
                    sql += ' WHERE ' + where
            if self.server == sqlite3:
                cursor = self.conn.execute(sql, tuple(condition.values()))
                rows = cursor.fetchall()
            else:
                with self.conn:
                    with self.conn.cursor() as cursor:
                        cursor.execute(sql, tuple(condition.values()))
                        rows = cursor.fetchall()
            if rows:
                return rows
        except self.server.Error as e:
            self.conn.rollback()
            return f"Error: {e}"

    def insert(self, table, data):
        self.connect_db()
        keys = ','.join(data.keys())
        values = ','.join(['?'] * len(data))
        try:
            sql = f"INSERT INTO {table}({keys}) VALUES({values});"
            if self.conn.execute(sql, tuple(data.values())):
                self.conn.commit()
        except self.server.Error as ex:
            self.conn.rollback()
            return f"Error:{ex}"

    def update(self, table, data, **condition):
        self.connect_db()
        s = ""
        for k, v in data.items():
            s += f"{k}='{v}',"
        s = s[:-1]
        sql = f"UPDATE {table} SET {s}"
        where = f" WHERE {','.join(condition.keys())}={','.join(['?'])};"
        sql += where
        try:
            if self.conn.execute(sql, tuple(condition.values())):
                self.conn.commit()
        except self.server.Error as ex:
            self.conn.rollback()
            return f"Error:{ex}"

    def delete(self, table, **condition):
        self.connect_db()
        sql = f"DELETE FROM {table}"
        where = f" WHERE {','.join(condition.keys())}={','.join(['?'])};"
        sql += where
        try:
            if self.conn.execute(sql, tuple(condition.values())):
                self.conn.commit()
        except self.server.Error as ex:
            self.conn.rollback()
            return f"Error:{ex}"

    def just_exe(self, sql):
        try:
            if self.server == sqlite3:
                with self.conn.execute(sql) as cursor:
                    return cursor.fetchall()
            else:
                with self.conn:
                    with self.conn.cursor() as cursor:
                        cursor.execute(sql)
                        return cursor.fetchall()
        except self.server.Error as ex:
            return f"Error:{ex}"

    # def upsert(self, table, data, constraint: int = None):
    #     """
    #     insert or update data into table in database
    #     @param table: str, table's name.
    #     @param data: dict, data's form.
    #     @param constraint: int, primary key's index of data, alternative. sqlite3 NEEDED.
    #     @return: None, except for error message.
    #     """
    #     keys = ','.join(data.keys())
    #     values = ','.join(['?'] * len(data))
    #     update = ','.join([f" {key}=?" for key in data])
    #     try:
    #         if self.server == sqlite3:
    #             sql = f'INSERT INTO {table}({keys}) VALUES({values}) ON CONFLICT({list(data.keys())[constraint]}) DO UPDATE SET'
    #         else:
    #             sql = f'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'
    #         sql += update
    #         print(sql)
    #         if self.conn.execute(sql, tuple(data.values()) * 2):
    #             self.conn.commit()
    #     except self.server.Error as e:
    #         self.conn.rollback()
    #         return f"Error: {e}"
