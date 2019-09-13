
from orm_pool.db_pool import POOL
import pymysql

class Mysql(object):
    # 键连接
    def __init__(self):
        self.conn = POOL.connection()

        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def db_close(self):
        self.cursor.close()
        self.conn.close()

    # def select(self,sql,args=None):
    #     self.cursor.execute(sql,args)  # 执行这个任务
    #
    #     res = self.cursor.fetchall()
    #     return res
    def select(self,sql,args=None):
        self.cursor.execute(sql,args)
        res = self.cursor.fetchall()
        return res

    def execute(self,sql,args):
        try:
            self.cursor.execute(sql,args)
        except BaseException as e:
            print(e)
