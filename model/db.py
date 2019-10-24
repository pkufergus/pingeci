import MySQLdb
from util.util import log
import threading



class Mysql(object):
    def __init__(self,host,port,user,passwd,db,charset='utf8'):
        try:
            self.conn = MySQLdb.connect(host,user,passwd,db,int(port), charset=charset)
        except MySQLdb.Error as e:
            errormsg = 'Cannot connect to server\nERROR(%s):%s' % (e.args[0],e.args[1])
            print(errormsg)
            exit(2)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()
        self.wlock = threading.Lock()

    def exec_write(self, sql):
        """exec dml,ddl"""
        log.info("mysql write")
        self.lock.acquire()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            errormsg = 'write db ERROR(%s):%s' % (e.args[0], e.args[1])
            print(errormsg)
            log.fatal("err={} sql={}".format(errormsg, sql))
            self.conn.rollback()
        finally:
            self.lock.release()

    def query(self, sql):
        """query """
        self.lock.acquire()
        results = []
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except Exception as e:
            errormsg = 'query db ERROR(%s):%s' % (e.args[0], e.args[1])
            print(errormsg)
            log.fatal("err={} sql={}".format(errormsg, sql))
        finally:
            self.lock.release()
        return results

mydb = None
if not mydb:
    mydb = Mysql("10.156.102.16", "8306", "root", "root", "music")

artistdb = None
if not artistdb:
    artistdb = Mysql("10.156.102.16", "8306", "root", "root", "music")

onlinedb = None
if not onlinedb:
    onlinedb = Mysql("10.156.102.16", "8306", "root", "root", "music")


