#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, abort, render_template, jsonify
from restful_apis import app
import sys
sys.path.append('/home/czw/MySimpleWeb/transwarp')
import db
from models import Employ, Student, Course

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/garde')
def garde():
    return render_template('garde.html')

@app.route('/api/failcount')
def fail_count():
    """
    统计不及格人数,默认输出全部科目
    """
    #是否过滤科目
    filter_course = request.args.get('course')
    if filter_course:
        datas = Employ.find_by('where cname="%s"' % filter_course)
    else:
        datas = Employ.find_all()
    fails = []
    for data in datas:
        if int(data['garde']) < 60:
            fails.append(data)
    return jsonify(fails)

@app.route('/api/honors')
def honor_count():
    """
    奖励统计
    """
    pass


if __name__ == '__main__':
    db.create_engine('root', 'woaini520', 'university')
    with db.connection():
        app.run(host='0.0.0.0')


