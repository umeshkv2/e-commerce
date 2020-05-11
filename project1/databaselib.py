import pymysql
def getdbcur():
    conn = pymysql.connect(host='db4free.net',
                                                port = 3306,
                                                user = 'umeshkv2',
                                                passwd = 'umeshkv2',
                                                db = 'multikart',
                                                autocommit = True)
    cur = conn.cursor()
    return cur