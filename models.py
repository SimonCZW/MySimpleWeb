#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/czw/MySimpleWeb/transwarp')
import db #import create_engine, connection, execute_sql
from orm import Model, StringField, IntegerField, FloatField, DateField

class Course(Model):
    cid = StringField(primary_key = True)
    cname = StringField()
    chours = IntegerField()
    credit = FloatField()
    precid = StringField()

class Student(Model):
    sid = IntegerField(ddl='bigint', primary_key=True)
    sname = StringField()
    sex = StringField()
    birthplace = StringField()
    birthdate = DateField()
    department = StringField()
    sclass = StringField()

class Employ(Model):
    sid = IntegerField(primary_key=True)
    sname = StringField()
    cid = StringField(primary_key=True)
    cname = StringField()
    garde = IntegerField()

if __name__ == '__main__':
    db.create_engine('root', 'woaini520', 'university')
    with db.connection():
        d={'sid':'3113000816', 'cid':'a2'}
        print Employ.get(d)
        #c = {'cid':'a2', 'cname':'eng', 'chours':'80', 'credit':'2.0', 'precid':'b2'}
        #course1 = Course(**c)
        #course1.update()
        #e = {'sid':'3113000816', 'cid':'a2', 'garde':'99'}
        #em1 = Employ(**e)
        #em1.update()



