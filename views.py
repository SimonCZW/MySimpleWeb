#!/usr/bin/python
# -*- coding:utf-8 -*-

#from flask import Flask, url_for, request, render_template, make_response, jsonify
from flask import Flask, request, abort
from flask.ext.restful import Resource, Api, reqparse, fields, marshal_with
from models import Student, Course, Employ
import sys
sys.path.append('/home/czw/MySimpleWeb/transwarp')
import db
import datetime

app = Flask(__name__)
api = Api(app)

#@app.route('/')
#def index():
#    return render_template('index.html')
#@app.route('/api/students')
#def api_get_users():
#    d={'a':'A'}
#    return jsonify(d)#{'a':'A'})

#构造REST API

db.create_engine('root', 'woaini520', 'university')
parser = reqparse.RequestParser()

student_fields = {
    'sid':  fields.Integer,
    'sname': fields.String,
    'sex':  fields.String,
    'birthplace':   fields.String,
    'birthdate':    fields.DateTime(dt_format='iso8601'),
    'department':   fields.String
}

class StudentAdd(Resource):
    #@marshal_with(student_fields)
    def get(self):
        """
        返回列表
        """
        datas =  Student.find_all()
        #判断是否为空
        if datas != []:
            #datetime.date转换为str,使得可以jsonify
            for data in datas:
                data['birthdate'] = datetime.datetime.strftime(data['birthdate'], '%Y%m%d')
            return datas
        else:
            return "None data"

    def post(self):
        """
        新增数据
        """
        parser.add_argument('sid', type=int)
        parser.add_argument('sname', type=str)
        parser.add_argument('sex', type=str)
        parser.add_argument('birthplace', type=str)
        parser.add_argument('birthdate', type=str)
        parser.add_argument('department', type=str)
        args = parser.parse_args()
        #判断输入完整性
        for key,value in args.iteritems():
            if value is None:
                return "Please input %s" % key  #写错误模块
        #判断是否插入成功
        stu = Student(**args)
        insert_row = stu.insert()
        if insert_row == 1: #向上抓取error判断
            return stu
        else:
            return "insert error" #写错误模块返回

class StudentResource(Resource):
    #@marshal_with(student_fields)
    def get(self, sid):
        """
        获取一指定sid数据,Student表主键为sid
        """
        data = Student.get({'sid':sid})
        if data is not None:
            #datetime.date转换为str,使得可以jsonify
            data['birthdate'] = datetime.datetime.strftime(data['birthdate'], '%Y%m%d')
            return data
        else:
            return "No data sid"

    def put(self, sid):
        """
        用于修改sid对应的数据行, 表单只需填写需要修改的数据项即可
        """
        parser.add_argument('sid', type=int)
        parser.add_argument('sname', type=str)
        parser.add_argument('sex', type=str)
        parser.add_argument('birthplace', type=str)
        parser.add_argument('birthdate', type=str)
        parser.add_argument('department', type=str)
        args = parser.parse_args()
        ModifyStudent = Student.get({'sid': sid})
        #判断是否存在数据
        if ModifyStudent is None:
            return "no sid data for modify(put)"
        #若表单给出sid,此sid与url对应不同报错
        if args['sid'] is not None and args['sid'] != sid:
            return "url's sid is not equal to form sid"
        ModifyStudent['birthdate'] = datetime.datetime.strftime(ModifyStudent['birthdate'], '%Y%m%d')
        for key, value in args.iteritems():
            if value is not None:
                ModifyStudent[key] = value
        update_row = ModifyStudent.update()
        if update_row == 1:
            return ModifyStudent
        else:
            return "update error"

    def delete(self, sid):
        """
        删除sid对应数据行
        """
        OldStudent = Student.get({'sid':sid})
        #判断是否有sid对应数据
        if OldStudent is None:
            return "no sid data for deleted"
        delete_row = OldStudent.delete()
        if delete_row == 1:
            return 'success delete %s' % sid, 200
        else:
            return 'cannot delete %s' % sid #接收上抛错误

api.add_resource(StudentAdd, '/students')
api.add_resource(StudentResource, '/students/<int:sid>')

if __name__ == '__main__':
    with db.connection():
        app.run(host='0.0.0.0')



