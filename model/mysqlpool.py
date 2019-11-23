import MySQLdb
from DBUtils.PooledDB import PooledDB
from util.util import log


class MysqlPool(object):
    host = '10.156.102.16'
    user = 'root'
    port = 8306
    pasword = 'root'
    db = 'music'
    charset = 'utf8'

    pool = None
    limit_count = 3  #limit

    def __init__(self):
        self.pool = PooledDB(MySQLdb, self.limit_count, host=self.host, user=self.user, passwd=self.pasword, db=self.db,
                             port=self.port, charset=self.charset, use_unicode=True)

    def exec_write(self, sql):
        """exec dml,ddl"""
        log.info("mysql write")
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            errormsg = 'write db ERROR(%s):%s' % (e.args[0], e.args[1])
            log.fatal("err={} sql={}".format(errormsg, sql))
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def query(self, sql):
        """query """
        results = []
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except Exception as e:
            errormsg = 'query db ERROR(%s):%s' % (e.args[0], e.args[1])
            log.fatal("err={} sql={}".format(errormsg, sql))
        finally:
            cursor.close()
            conn.close()
        return results


mypool = None
if not mypool:
    mypool = MysqlPool()
