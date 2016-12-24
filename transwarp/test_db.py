#!/usr/bin/python
# -*- coding:utf-8 -*-
import db

db.create_engine('root', 'woaini520', 'university')
#双层with,测试可在__enter__和__exit__中插入输出观察.
#这里为第一层with,第二层为_select的装饰器.
with db.connection():
    #BASE TEST 1
    #select
    #print db.select_count("select count(*) from ?", 'Course')
    #print db.select_one("select * from ?", 'Course')
    #print db.select("select * from ?", 'Course')

    #insert
    print db._update("insert into Course values('?', '?', '?')",
                    'a2', 'ng', 'b2')

    #delete
    #print db.update("delete from Course where cid = '?'", 'a4')

    #update
    #print db.update("update Course set cname = '?' where cid = '?'",
    #                'x', 'a3')
