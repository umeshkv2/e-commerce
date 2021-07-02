import pymysql
def getdbcur():
    conn = pymysql.connect(host='sql6.freesqldatabase.com',
                                                port = 3306,
                                                user = 'sql6422566',
                                                passwd = 'jmNxpKMPip',
                                                db = 'sql6422566',
                                                autocommit = True)
    cur = conn.cursor()
    return cur
