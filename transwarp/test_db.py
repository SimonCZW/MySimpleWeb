#!/usr/bin/python
# -*- coding:utf-8 -*-
import db

db.create_engine('root', 'woaini520', 'university')
#双层with,测试可在__enter__和__exit__中插入输出观察.
#这里为第一层with,第二层为_select的装饰器.
with db.connection():
    print db.select_count("select count(*) from ?", 'Course')
    print db.select_count("select count(*) from ?", 'Student')

