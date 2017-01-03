#!/usr/bin/python
# -*- coding:utf-8 -*-
import db

def _gen_sql(table, mappings):
    """
    生成表的sql
    """
    #print "table:", table
    #for k,v in mappings.iteritems():
    #    print "k: %s, v: %s" % (k, v)
    sql = 'create table %s(' % (table,)
    #sorted高阶函数,前为排序值,后面为排序算法函数
    for field in sorted(mappings.values(), lambda x,y: cmp(x._order,y._order)):
        if not hasattr(field, 'ddl'):
            raise  StandardError('no ddl in field "%s".' % field.name)
        if field.nullable:
            DDL = field.name + " " + field.ddl + ","
        else:
            DDL = field.name + " " + field.ddl + " " + "not null,"
        sql = sql+DDL
        if field.primary_key:
            pk =  field.name
    sql=sql+' primary key('+pk+') );'
    return sql

class Field(object):
    _count = 0 #用于记录xxxField()顺序,建表时使用.
    def __init__(self, **kw):
        self.name = kw.get('name', None)
        self.primary_key = kw.get('primary_key', False)
        self.ddl = kw.get('ddl', '')
        self.nullable=  kw.get('nullable', False)
        self._default = kw.get('defalut', None)
        self._order = Field._count
        Field._count += 1
    def __str__(self):
        return "<%s:%s,%s,default(%s)>" % (self.__class__.__name__
                    , self.name, self.ddl, self._default)

class StringField(Field):
    def __init__(self, **kw):
        if 'default' not in kw:
            kw['default'] = ''
        if 'ddl' not in kw:
            kw['ddl'] = 'varchar(255)'
        super(StringField, self).__init__(**kw)

class DateField(Field):
    def __init__(self, **kw):
        if 'defalut' not in kw:
            kw['default'] = ''
        if 'ddl' not in kw:
            kw['ddl'] = 'date'
        super(DateField, self).__init__(**kw)

class IntegerField(Field):
    def __init__(self, **kw):
        if 'default' not in kw:
            kw['default'] =  0
        if 'ddl' not in kw:
            kw['ddl'] = 'int'
        super(IntegerField, self).__init__(**kw)

class FloatField(Field):
    def __init__(self, **kw):
        if 'default' not in kw:
            kw['default'] =  0.0
        if 'ddl' not in kw:
            kw['ddl'] = 'float'
        super(FloatField, self).__init__(**kw)

class BooleanField(Field):
    def __init__(self, **kw):
        if 'default' not in kw:
            kw['default'] =  False
        if 'ddl' not in kw:
            kw['ddl'] = 'bool'
        super(BooleanField, self).__init__(**kw)

class TextField(Field):
    def __init__(self, **kw):
        if 'default' not in kw:
            kw['default'] = ''
        if 'ddl' not in kw:
            kw['ddl'] = 'text'
        super(TextField, self).__init__(**kw)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        #一开始创建Model类跳过
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        primary_keys = []
        for k,v in attrs.iteritems():
            if isinstance(v, Field):
                #v-Field设置默认name字段
                if not v.name:
                    v.name = k
                mappings[k] = v
                #确定primary_key
                if v.primary_key:
                    primary_keys.append(v.name)
        #检查是否有primary_key
        if not primary_keys:
            raise TypeError('Primary key is not defined in class: %s' % name)
        #移除已经放到mappings中的属性xxxField
        for k in mappings.iterkeys():
            attrs.pop(k)
        #加入new attribute
        if not '__table__' in attrs:
            attrs['__table__'] = name #默认表名为类名
        attrs['__create_sql__'] = lambda self: _gen_sql(attrs['__table__'], mappings)
        attrs['__primary_key__'] =  primary_keys
        attrs['__mappings__'] = mappings
        return type.__new__(cls, name, bases, attrs)

class Model(dict):

    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key]=value

    @classmethod
    def get(cls, primary_keys):
        """
        用法:user = User.get('{primary_key:value}')
        primary_keys为字典
        """
        #data = db.select_one('select * from %s where %s="?"' %
        #    (cls.__table__, cls.__primary_key__), primary_key)
        #多primary_key:
        sql = ['select * from %s where ' % cls.__table__]
        for k,v in primary_keys.iteritems():
            sql.append('%s = "%s"' % (k, v))
            if k != primary_keys.keys()[-1] :
                sql.append(' and ')
        sql=''.join(sql)
        data = db.select_one(sql)
        return cls(**data) if data else None

    @classmethod
    def find_first(cls, where='', *args):
        """
        where语句条件查询,返回第一个
        用法: Class.find_first(where)
        """
        d = db.select_one('select * from %s %s' % (cls.__table__, where), *args)
        return cls(**d) if d else None

    @classmethod
    def find_all(cls, *args):
        """
        用法: Class.find_all()
        """
        L = db.select('select * from %s' % cls.__table__)
        return [cls(**d) for d in L]

    @classmethod
    def find_by(cls, where='', *args):
        """
        用法: Class.find_by(where),返回全部对象组成List
        """
        L = db.select('select * from %s %s' % (cls.__table__, where), *args)
        return [cls(**d) for d in L]

    @classmethod
    def count_all(cls):
        """
        用法: Class.count_all(),返回此类对应表的数据行数
        """
        return db.select_count('select count(*) from %s' % (cls.__table__))

    @classmethod
    def count_by(cls, where='', *args):
        """
        用法: Class.count_by(where),根据查询条件where返回行数
        """
        return db.select_count('select count(*) from %s %s' %
                (cls.__table__, where), *args)

    def insert(self):
        """
        存入数据库
        """
        params = {}
        #获取字段对应值
        #类中定义字段 x = xxxField() => k=x , v=xxxField()
        for k,v in  self.__mappings__.iteritems():
            #v.name指 k=xxField(name='uu')设置的值uu,默认为k
            params[v.name] =  self[k]
        #存入数据库
        row = db.insert(self.__table__, **params)
        #return self
        return row

    def update(self):
        """
        更新数据库,更新修改项
        """
        params = {}
        for k,v in self.__mappings__.iteritems():
            params[v.name] = self[k]
        row = db.update(self.__table__, self.__primary_key__, **params)
        return row

    def delete(self):
        #获取主键对应xxxField的名字
        #primary_key_name = self.__mappings__.get(self.__primary_key__).name
        #primary_value = self[primary_key_name]
        #delete_row = db.delete(self.__table__, self.__primary_key__, primary_value)
        params = {}
        for k,v in self.__mappings__.iteritems():
            params[v.name] = self[k]
        delete_row = db.delete(self.__table__, self.__primary_key__, **params)
        #return self
        return delete_row


if __name__ == '__main__':
    class Course(Model):
        """
        主要xxxField的name属性为建表的属性,不然出错
        """
        cid = StringField(primary_key=True)
        cname = StringField()
        chours = IntegerField()
        credit = FloatField()
        precid = StringField()

    db.create_engine('root', 'woaini520', 'university')

    course = {'cid':'a1'}
    print Course.get(**course)
    #with db.connection():
        #db.execute_sql('create table Course(cid char(20) primary key,cname char(20),precid char(20))')
        #db.execute_sql('create table Student(sid int primary key, sname char(20) not null,sex ENUM("m","w"),birthday date,department char(20))')
        #db.execute_sql('create table Employ(sid int not null,cid char(20) not null,garde int,primary key(sid, cid),foreign key(sid) references Student(sid),foreign key(cid) references Course(cid))')
        #db.execute_sql('drop table if exists Course')
        #db.execute_sql('drop table if exists Student')
        #db.execute_sql('drop table if exists Employ')

    #print Course().__create_sql__()

    #course=Course(cid='a7', cname='orm2fix', precid='c2')
    #kw = {'cname': 'orm2fix', 'cid': 'a7', 'precid': 'c2'}
    #user = User(**kw)
    #print course
    #with db.connection():
    #course.insert()
    #course.delete()
    #    user.update()
    #print User.get('a7')
    #print Course.count_all()
    #print User.count_by()
    #print User.count_by('where cname="orm2fix"')
    #print User.find_first('where cname="orm2fix"')
    #print User.find_all()
    #print User.find_by('where cname="orm2fix"')



