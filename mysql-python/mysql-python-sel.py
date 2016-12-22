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
sql = 'select * from Course'
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        #print row
        cid = row[0]
        cname = row[1]
        precid = row[2]
        print "cid=%s, cname=%s, precid=%s" % (cid, cname, precid)
except Exception,e:
    print e
    db.rollback()
db.close()

