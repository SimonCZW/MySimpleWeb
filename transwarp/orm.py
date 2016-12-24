#!/usr/bin/python
# -*- coding:utf-8 -*-
import db

class Field(object):
    def __init__(self, **kw):
        self.name = kw.get('name', None)
        self.primary_key = kw.get('primary_key', False)
    def __str__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, **kw):
        super(StringField, self).__init__(**kw)

class IntegerField(Field):
    def __init__(self, **kw):
        super(IntegerField, self).__init__(**kw)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        #一开始创建Model类跳过
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k,v in attrs.iteritems():
            if isinstance(v, Field):
                #v-Field设置默认name字段
                if not v.name:
                    v.name = k
                mappings[k] = v
                #确定primary_key
                if v.primary_key:
                    primary_key = v.name
        #移除已经放到mappings中的属性xxxField
        for k in mappings.iterkeys():
            attrs.pop(k)
        #加入new attribute
        attrs['__primary_key__'] = v.name
        attrs['__mappings__'] = mappings
        #print attrs
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
    def get(cls, primary_key):
        """
        用法:user = User.get('primary_key')
        """

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
        return self

    def update(self):
        """
        更新数据库,更新修改项
        """
        params = {}
        for k,v in self.__mappings__.iteritems():
            params[v.name] = self[k]
        row = db.update(self.__table__, self.__primary_key__, **params)
        return self

    def delete(self):
        #获取主键对应xxxField的名字
        #primary_key_name = self.__mappings__.get(self.__primary_key__).name
        #primary_value = self[primary_key_name]
        #delete_row = db.delete(self.__table__, self.__primary_key__, primary_value)
        params = {}
        for k,v in self.__mappings__.iteritems():
            params[v.name] = self[k]
        delete_row = db.delete(self.__table__, self.__primary_key__, **params)
        return self

    def find_first(self):
        pass

    def find_all(self):
        pass

    def find_by(self):
        pass

    def count_all(self):
        pass

    def count_by(self):
        pass



if __name__ == '__main__':
    class User(Model):
        __table__ = 'Course'
        #id = IntegerField(name='ID', primary_key=True)
        cid = StringField()
        cname = StringField()
        precid = StringField()

    db.create_engine('root', 'woaini520', 'university')
    user=User(cid='a7', cname='orm2fix', precid='c2')
    with db.connection():
        user.insert()
        user.delete()
        user.update()

    #print user.mappings
    #print user










