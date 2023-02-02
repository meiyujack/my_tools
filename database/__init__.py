import sqlite3


class Database:
    def __init__(self, server, **kwargs):
        """
        Initialize basic information about current database.
        @param server: database name, like mariadb, sqlite3, etc.
        @param kwargs: key=value. if sqlite,file_address and sql_address in case want to reconstruct table;
        if mariadb, host={host}, user={user}, etc.
        """
        self.server = server
        for k, v in kwargs.items():
            self.k = v

    def connect_db(self):
        """
        Connect to the database.
        @return: None, except for error message.
        """
        try:
            if self.server == "sqlite":
                return sqlite3.connect(self.file_address)
            return self.server.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
        except self.server.Error as e:
            return e

    def init_table(self, conn):
        """
        Initialize table schema structure.
        @param conn: database's Connection.
        """
        with open(self.sql_address, mode="r") as file:
            conn.cursor().executescript(file.read())
            conn.commit()
            print("Initialize database completed.")

    def select_db(self, conn, table, get='*', prep=None, **condition):
        """
        Just execute "select" sentence.
        @param conn: database's Connection.
        @param table: str, table's name.
        @param get: str, default: *, what column or property you want to get.
        @param prep: str, default:None, prep. "and" or "or(secondly)" in WHERE clause. At most two conditions now.
        @param condition: **condition, according to what condition you want to find.
        @return: rows if execute select sentence or error message.
        """
        cursor = conn.cursor()
        sql = f"SELECT {get} FROM {table}"
        where = f" WHERE {','.join(condition.keys())}={','.join(['?'])}"
        if len(condition) == 1:
            sql += where
        else:
            where = f' {prep} '.join(
                [f"{''.join(m.keys())}={''.join(['?'])}" for m in [{i: j} for i, j in condition.items()]])
            sql += ' WHERE ' + where
        try:
            cursor.execute(sql, tuple(condition.values()))
            rows = cursor.fetchall()
            if rows:
                return rows
            # else:
            #     self.conn.commit()
        except self.server.Error as e:
            conn.rollback()
            return f"Error: {e}"

    def upsert(self, conn, table, data, constraint: int = None):
        """
        insert or update data into table in database.
        @param conn: database's Connection.
        @param table: str, table's name.
        @param data: dict, data's form.
        @param constraint: int, primary key's index of data, alternative, especially for sqlite3's update sentence.
        @return: None, except for error message.
        """
        keys = ','.join(data.keys())
        values = ','.join(['?'] * len(data))
        update = ','.join([f" {key}=?" for key in data])
        try:
            if self.server == "sqlite":
                sql = f'INSERT INTO {table}({keys}) VALUES({values}) ON CONFLICT({list(data.keys())[constraint]}) DO UPDATE SET'
            else:
                sql = f'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'
            sql += update
            print(sql)
            if conn.execute(sql, tuple(data.values()) * 2):
                conn.commit()
        except self.server.Error as e:
            conn.rollback()
            return f"Error: {e}"
