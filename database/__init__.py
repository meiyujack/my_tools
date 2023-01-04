import sqlite3


class Database:
    def __init__(self, server, **kwargs):
        """
        Initialize basic information about current database.
        @param server: database name, like mariadb, sqlite3, etc.
        @param kwargs: key=value,if mariadb, host={host}, user={user}, etc.
        """
        self.server = server
        self.file_address = kwargs.get('file_address')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port', 3306)
        self.database = kwargs.get('database')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.conn = None

    def connect_db(self):
        """
        Connect to the database.
        @return: db's connection
        """
        try:
            if self.server == "sqlite":
                self.conn = sqlite3.connect(self.file_address)
                return None
            self.conn = self.server.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return None
        except self.server.Error as e:
            return e

    def execute_db(self, sql):
        """
        Just execute command. especially in select sentence.
        @param sql: str, sql command.
        @return: rows if execute select sentence or error message.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                return rows
            else:
                self.conn.commit()
        except self.server.Error as e:
            self.conn.rollback()
            return f"Error: {e}"

    def upsert(self, table, data, constraint: int = None):
        """
        insert or update data into table in database.
        @param table: str, table's name.
        @param data: dict, data's form.
        @param constraint: int, key's index of data, alternative, especially for sqlite3's update sentense.
        @return: str, message if error.
        """
        cursor = self.conn.cursor()
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
            if self.conn.execute(sql, tuple(data.values()) * 2):
                self.conn.commit()
        except self.server.Error as e:
            self.conn.rollback()
            return f"Error: {e}"
