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

@app.route('/api/sclass')
def getsclass():
    """
    统计各班总分和平均分,并按平均分排序
    {
  "auto1_eng": {
    "count": 4,
    "total_garde": 320
  },
  "auto2_en": {
    "count": 1,
    "total_garde": 70
  },
  "auto2_eng": {
    "count": 1,
    "total_garde": 70
  }
}
    """
    datas = Employ.find_all()
    sclass = {}
    count = 1
    sclass_type = []
    for data in datas:
        #初始化数据
        identify=str(data['sclass'])+'_'+str(data['cname'])
        if identify not in sclass_type :
            sclass_type.append(identify)
            #sclass[data['sclass']][data['cname']]={'total_garde':int(data['garde']), 'count':count}
            #sclass[str(data['sclass'])+str(data['cname'])] = {'total_garde':int(data['garde']), 'count':count}
            sclass[identify] = {'total_garde':int(data['garde']), 'count':count}
        else:
            #sclass[data['sclass']][data['cname']]['total_garde'] += int(data['garde'])
            #sclass[data['sclass']][data['cname']]['count'] += 1
            #sclass[str(data['sclass']+str(data['cname'])]['total_garde'] += int(data['garde'])
            #sclass[str(data['sclass']+str(data['cname'])]['count'] += 1
            sclass[identify]['total_garde'] += int(data['garde'])
            sclass[identify]['count'] += 1
    class_total_garde = {}
    #插入平均分
    for class_course,value in sclass.iteritems():
        #班级每科的平均分
        sclass[class_course]['avg_garde'] =  value['total_garde']/value['count']
        #获取班级和课程名
        sclass_name, course = class_course.split('_')
        if sclass_name not in class_total_garde:
            class_total_garde[sclass_name]={}
            class_total_garde[sclass_name]['avg_total_garde'] = sclass[class_course]['avg_garde']
            class_total_garde[sclass_name]['course_count'] = 1
        else:
            class_total_garde[sclass_name]['avg_total_garde'] += sclass[class_course]['avg_garde']
            class_total_garde[sclass_name]['course_count'] += 1
    for sclass_name, value in class_total_garde.iteritems():
        class_total_garde[sclass_name]['avg_garde'] = value['avg_total_garde']/value['course_count']
    #sort_by = request.args.get('sortby')
    #order = request.args.get('order', 'desc')
    #if sort_by:
    #    #升序
    #    if order == 'asc':
    #        return jsonify(sorted(value, lambda x,y: cmp(x[sort_by], y[sort_by])))
    #    #降序
    #    if order == 'desc':
    #        #class_total_garde = sorted(value, lambda x,y: cmp(y[sort_by],x[sort_by]))
    #        return jsonify(sorted(value, lambda x,y: cmp(y[sort_by],x[sort_by])))
    return jsonify(class_total_garde)
    #return jsonify(sclass)

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


