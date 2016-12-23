#!/usr/bin/python
# -*- coding:utf8 -*-
import threading
import MySQLdb
import functools

#全局调用engine
engine = None

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

def connection():
    return _ConnectionCtx()

def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper

@with_connection
def _select(sql, single=False, *args):
    global _dbctx
    cursor = None
    sql = sql.replace('?', '%s')

    try:
        cursor = _dbctx.connection.cursor()
        cursor.execute(sql % args)
        names = [ x[0] for x in cursor.description]
        if single:
            values = cursor.fetchone()
            if not values:
                return None
            return Dict(names, values)
        return [Dict(names, values) for values in cursor.fetchall()]
    except Exception,e:
        raise SelectError(e)
    finally:
        if cursor:
            cursor.close()

def select(sql,*args):
    return _select(sql, False, *args)

def select_one(sql, *args):
    return _select(sql, True, *args)

def select_count(sql, *args):
    """
    用于select count(*) from Table,返回行数
    """
    _data = _select(sql, True, *args)#{'count(*)':n}
    if len(_data) != 1:
        raise MultiColumnsError('Expect only one column.')
    return _data.values()[0]

class Dict(dict):
    """
    字典对象,扩展实现传入两个元组将其对应放入字典k-v
    """
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k,v in zip(names, values):
            self[k] = v

        def __getattr__(self, key):
            try:
                return self[key]
            except KeyError:
                raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

        def __setattr__(self, key, value):
            self[key] = value

class DBError(Exception):
    def __init__(self, meessage):
        return message

class SelectError(Exception):
    def __init__(self, message):
        return message

class MultiColumnsError(Exception):
    def __init__(self, message):
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

class _LasyConnection(object):
    """
    封装获取数据库engine,返回惰性连接对象,只有调用是才连接返回游标
    """
    def __init__(self):
        self.connection = None

    def cursor(self):
        #global engine
        if self.connection is None:
            _connection = engine.connect()
            self.connection = _connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            _connection.close()

class _Dbctx(threading.local):
    """
    真正连接数据,获取惰性连接
    """
    def __init__(self):
        self.connection = None

    def is_not_init(self):
        return self.connection is None

    def is_init(self):
        return self.connection is not None

    def init(self):
        self.connection = _LasyConnection()

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

_dbctx = _Dbctx()
class _ConnectionCtx(object):
    """
    auto connect and close
    """
    def __enter__(self):
        """
        获取惰性连接
        """
        global _dbctx
        self.should_clean = False
        print "__enter__"
        #fix bug:
        #error syntx :if not _dbctx.is_init: 返回了一个函数对象为true,导致出错
        #right : if not _dbctx.is_init(): 有括号函数返回了结果False
        if _dbctx.is_not_init():
            print "init"
            _dbctx.init()
            self.should_clean = True
        return self

    def __exit__(self, type, value, trace):
        """
        释放连接
        """
        global _dbctx
        print "__exit__"
        if self.should_clean:
            print "cleanup"
            _dbctx.cleanup()
            self.should_clean = False


if __name__ == '__main__':
    create_engine('root', 'woaini520', 'university')

    #sql = "select * from ?"
    #data = select(sql, 'Course')
    #print data

    sql = "select count(*) from ?"
    print select_count(sql, 'Course')

    # _select test ok
    #Single line
    #print _select(sql, True ,'Course')
    #print select_one(sql, 'Course')
    #all
    #print _select(sql, False ,'Course')
    #print select(sql, 'Course')

    #engine test ok
    #connection = engine.connect()
    #cursor = connection.cursor()
    #sql = "select * from Course"
    #cursor.execute(sql)
    #print cursor.fetchone()

    #_LasyConnection() test ok
    #connect = _LasyConnection()
    #con = connect.cursor()

    #_Dbctx() test ok
    #if not _dbctx.is_init():
    #    _dbctx.init()
        #print _dbctx.cursor()
    #con = _dbctx.cursor()
    #sql = "select * from Course"
    #con.execute(sql)
    #print con.fetchone()



