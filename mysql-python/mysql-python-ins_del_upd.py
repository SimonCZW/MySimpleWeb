#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb
db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='woaini520',
    db='university',
    charset='utf8')

cursor = db.cursor()
print cursor.description
cursor.execute("select count(*) from Course")
data=cursor.fetchone()
print data
#sql = 'insert into Course(cid, cname) values("b1", "english")'
#sql = 'insert into Course values("a1", "math", "b1")'
#sql = 'update Course set cname="x" where cid="b1"'
sql = 'delete from Course where cid="b1"'
try:
    cursor.execute(sql)
    db.commit()
except Exception,e:
    print e
    db.rollback()
db.close()

