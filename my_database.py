def get_connected(user, password, host, database, server, port=3306):
    try:
        db = server.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        print(f'{server}连接成功!')
        db.autocommit = False
        return db
    except server.Error as e:
        print(f"Error connecting to {server} Platform: {e}")


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
        if cursor.execute(sql, tuple(data.values())*2):
            db.commit()
    except server.Error as e:
        print(f"错误: {e}")
        db.rollback()
