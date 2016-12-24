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
        attrs['mappings'] = mappings
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

    def get(self):
        pass

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

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


class User(Model):
    __table__ = 'users'
    id = IntegerField(name='ID', primary_key=True)
    name = StringField(name='NAME')

user=User(name='test')
#print user.mappings
#print user










