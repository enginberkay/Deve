import sqlite3
from sqlite3 import Error

__conn = None

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def get_last_changeset_id():
    try:
        cur = __conn.cursor()
        sql_last_row_id = '''select max(id) from deploys d'''
        cur.execute(sql_last_row_id)
        last_row_id = cur.fetchone()
        sql = '''select end_changeset_id from deploys d where d.id = ?'''
        cur.execute(sql, (last_row_id[0],))
        last_changeset_id = cur.fetchone()
        return last_changeset_id[0]
    except Error as e:
        raise Exception(e)


def insert_deploys(deploy):
    try:
        sql = ''' INSERT INTO deploys(start_changeset_id,end_changeset_id,deployment_date)
                VALUES(?,?,?) '''
        cur = __conn.cursor()
        cur.execute(sql, deploy)
        __conn.commit()
        return cur.lastrowid
    except Error as e:
        __conn.rollback()
        print(e)

def insert_scripts(script):
    try:
        sql = ''' INSERT INTO scripts(deploy_id,script_name)
                VALUES(?,?) '''
        cur = __conn.cursor()
        cur.execute(sql, script)
        __conn.commit()
        return cur.lastrowid
    except Error as e:
        __conn.rollback()
        print(e)


def insert_script_results(result):
    try:
        sql = ''' INSERT INTO script_results(script_id,result)
                VALUES(?,?) '''
        cur = __conn.cursor()
        cur.execute(sql, result)
        __conn.commit()
        return cur.lastrowid
    except Error as e:
        __conn.rollback()
        print(e)


def __main():
    global __conn
    database = r"pythonsqlite.db"
    create_table_scripts = []
    create_table_scripts.append(open("sql/sqlite_create_deploy_table", "r").read())
    create_table_scripts.append(open("sql/sqlite_create_scripts_table", "r").read())
    create_table_scripts.append(open("sql/sqlite_create_script_results_table", "r").read())
    __conn = create_connection(database)
    if __conn is not None:
        for val in create_table_scripts:
           create_table(__conn, val)

if __name__ in ['__main__','SqliteManager']:
    __main()
