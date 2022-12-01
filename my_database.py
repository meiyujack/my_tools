from utils import open_file_as_txt
import sqlite3


def get_connected(**kwargs):
    """
    user, password, host, database, server,file_address, port=3306
    """
    if kwargs.get("server")==sqlite3:
        db=sqlite3.connect(kwargs.get("file_address"))
        return db
    try:
        db = kwargs.get("server").connect(
            user=kwargs.get("user"),
            password=kwargs.get("password"),
            host=kwargs.get("host"),
            port=kwargs.get("port"),
            database=kwargs.get("database")
        )
        print(f'{kwargs.get("server")}连接成功!')
        db.autocommit = False
        return db
    except kwargs.get("server").Error as e:
        print(f"Error connecting to {kwargs.get('server')} Platform: {e}")


def exec(server, db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        rows=cursor.fetchall()
        if rows:
            return rows
        else:
            db.commit()
    except server.Error as e:
        print(f"错误: {e}")
        db.rollback()


def in_or_up(server, db, table, data):
    cursor = db.cursor()
    keys = ','.join(data.keys())
    values = ','.join(['?'] * len(data))
    sql = f'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'
    update=','.join([f" {key}=?" for key in data])
    sql+=update
    try:
        print(sql)
        if cursor.execute(sql, tuple(data.values())*2):
            db.commit()
    except server.Error as e:
        print(f"错误: {e}")
        db.rollback()


