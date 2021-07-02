import pymysql
def getdbcur():
    conn = pymysql.connect(host='db4free.net',
                                                port = 3306,
                                                user = 'sql6.freesqldatabase.com',
                                                passwd = 'jmNxpKMPip',
                                                db = 'sql6422566',
                                                autocommit = True)
    cur = conn.cursor()
    return cur
