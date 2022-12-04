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

    def connect_db(self):
        """
        Connect to the database.
        @return: db's connection
        """
        try:
            if self.server == sqlite3:
                db = sqlite3.connect(self.file_address)
                return db
            db = self.server.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return db
        except self.server.Error as e:
            return e

    def execute_db(self, db, sql):
        """
        Just execute command. especially in select sentence.
        @param db: connection, connection of database.
        @param sql: str, sql command.
        @return: rows if execute select sentence or error message.
        """
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                return rows
            else:
                db.commit()
        except self.server.Error as e:
            db.rollback()
            return f"Error: {e}"

    def upsert(self, db, table, data):
        """
        insert or update data into table in database.
        @param db: connection, connection of database.
        @param table: str, table's name.
        @param data: dict, data's form.
        @return: str, message if error.
        """
        cursor = db.cursor()
        keys = ','.join(data.keys())
        values = ','.join(['?'] * len(data))
        update = ','.join([f" {key}=?" for key in data])
        try:
            if self.server == sqlite3:
                sql = f'INSERT INTO {table}({keys}) VALUES({values}) ON CONFLICT({keys}) DO UPDATE SET'
            else:
                sql = f'INSERT INTO {table}({keys}) VALUES({values}) ON DUPLICATE KEY UPDATE'
            sql += update
            if cursor.execute(sql, tuple(data.values()) * 2):
                db.commit()
        except self.server.Error as e:
            db.rollback()
            return f"错误: {e}"
