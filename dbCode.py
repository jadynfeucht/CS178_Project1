import pymysql
import creds

def get_conn():
    conn = pymysql.connect(
        host = creds.host,
        user = creds.user,
        password = creds.password,
        db = creds.db,
        )
    return conn

def execute_query(query, args=()):
    cur = get_conn().cursor(pymysql.cursors.DictCursor) # this is new
    cur.execute(query, args)
    rows = cur.ftechall()
    cur.close()
    return rows

def get_list_of_dictionaries(category):
    rows = execute_query("""SELECT *
                            FROM""")