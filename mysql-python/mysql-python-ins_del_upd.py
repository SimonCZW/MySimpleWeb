#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='password',
    db='university',
    charset='utf8')

cursor = db.cursor()
#print cursor.description
#cursor.execute("select count(*) from Course")
#data=cursor.fetchone()
#print data
#sql = 'insert into Course(precid, cname, cid) values("b8", "english2", "a8")'
sql = 'insert into Employ(sid, cid, garde) values("3", "a1", "80")'
#print sql
#sql = 'insert into Course values("a1", "math", "b1")'
#sql = 'update Course set cname="math2" where cid="a1"'
#sql = 'delete from Course where cid="b1"'
try:
    cursor.execute(sql)
    print cursor.rowcount
    db.commit()
except Exception,e:
    print e
    db.rollback()
db.close()

