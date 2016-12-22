#!/usr/bin/python
# -*- coding:utf8 -*-

#!/usr/bin/python
# -*- coding:utf-8 -*-
import MySQLdb

#全局调用engine
engine = None

class DBError(Exception):
    def __init__(message):
        return message

class _Engine(object):
    """
    数据库引擎对象，保存create_engine创建的数据连接
    使用_Engine.connect()调用
    """
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect

def create_engine(user, passwd, database, host='127.0.0.1', port=3306, **kw):
    """
    实现:
        from transwarp import db
        db.create_engine(user='root', password='password', database='test', host='127.0.0.1', port=3306)
    """

    global engine
    #如果已经初始化engine
    if engine is not None:
        raise DBError('Engine is already initialized')
    params = dict(user=user, passwd=passwd, db=database, host=host, port=port)
    #defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    defaults = dict(use_unicode=True, charset='utf8', autocommit=False)
    for k,v in defaults.iteritems():
       params[k] = kw.pop(k,v) #如果kw中有defaults中的键值对这剔除,且返回v
    params.update(kw) #将kw剩下的k-v加入params
    #params['buffered'] = True
    #engine = _Engine(lambda: MySQLdb.connect(**params)) #lambda会创建一个函数对象
    engine = _Engine(MySQLdb.connect(**params)) #lambda会创建一个函数对象

if __name__ == '__main__':
    create_engine('root', 'woaini520', 'university')

    connection = engine.connect()
    cursor = connection.cursor()
    sql = "select * from Course"
    cursor.execute(sql)
    print cursor.fetchone()






