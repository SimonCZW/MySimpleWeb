#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, abort
from flask.ext.restful import Resource, Api, reqparse, fields, marshal_with
from models import Student, Course, Employ
from  MySQLdb import IntegrityError, OperationalError
import sys
sys.path.append('/home/czw/MySimpleWeb/transwarp')
import db
import datetime

app = Flask(__name__)
api = Api(app)
#构造REST API
#@app.route('/')
#def index():
#    return render_template('index.html')
#@app.route('/api/students')
#def api_get_users():
#    d={'a':'A'}
#    return jsonify(d)#{'a':'A'})

db.create_engine('root', 'woaini520', 'university')

class StudentAdd(Resource):
    """
    获取所有学生数据或者新增一数据.
    curl http://localhost:port/students
    """
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
            return datas, 200
        else:
            return {'error': "has no student data"}, 404

    def post(self):
        """
        新增数据
        """
        parser = reqparse.RequestParser()
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
                return {'error': "Please input field: %s" % key }, 400
        stu = Student(**args)
        try:
            insert_row = stu.insert()
            #判断是否插入成功
            if insert_row == 1:
                return stu, 201
        except  IntegrityError ,e:
            #insert duplicate primary_key entry
            if e[0] == 1062:
                return {'primary error': e[1]}, 400
        except Exception,e:
            return {'error': e[1]}, 400

class StudentResource(Resource):
    """
    查询/修改/删除一数据.
    curl http://localhost:port/students/sid
    """
    def get(self, sid):
        """
        获取一指定sid数据,Student表主键为sid
        """
        data = Student.get({'sid':sid})
        if data is not None:
            #datetime.date转换为str,使得可以jsonify
            data['birthdate'] = datetime.datetime.strftime(data['birthdate'], '%Y%m%d')
            return data,200
        else:
            return {'error': "has no student data with sid: %s" % sid},404

    def put(self, sid):
        """
        用于修改sid对应的数据行, 表单只需填写需要修改的数据项即可
        """
        parser = reqparse.RequestParser()
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
            return {'error' : "has no student data with sid: %s for modify(put), please send post request to create first" % sid}, 404
        #若表单给出sid,此sid与url对应不同报错
        if args['sid'] is not None and args['sid'] != sid:
            return {'error' : "url's(put) sid(%s) is not equal to form sid(%s)" % (sid, args['sid'])},400
        ModifyStudent['birthdate'] = datetime.datetime.strftime(ModifyStudent['birthdate'], '%Y%m%d')
        for key, value in args.iteritems():
            if value is not None:
                ModifyStudent[key] = value
        try:
            update_row = ModifyStudent.update()
            if update_row == 1:
                return ModifyStudent,201
        except Exception,e:
            return {'error', e[1]},400

    def delete(self, sid):
        """
        删除sid对应数据行
        """
        OldStudent = Student.get({'sid':sid})
        #判断是否有sid对应数据
        if OldStudent is None:
            return {'error': "has no student data with sid: %s for deleted" % sid},404
        try:
            delete_row = OldStudent.delete()
            if delete_row == 1:
                return { 'success' : 'success delete data with sid:%s' % sid},204
        except IntegrityError,e:
            if e[0] == 1451:
                return {'foreign error':e[1]},400 #外键约束
            return {'error', e[1]},400
        except Exception,e:
            return {'error':e[1]},400

class CourseAdd(Resource):
    """
    查看/新增课程
    curl http://localhost:port/courses
    """
    def get(self):
        datas = Course.find_all()
        if datas != []:
            return datas,200
        else:
            return {'error': "has no course data"},404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid', type=str)
        parser.add_argument('cname', type=str)
        parser.add_argument('chours', type=int)
        parser.add_argument('credit', type=float)
        parser.add_argument('precid', type=str)
        args = parser.parse_args()
        for key,value in args.iteritems():
            if key == 'precid':
                continue
            if value is None:
                return {'error':"Please input field: %s" % key},400
        course = Course(**args)
        try:
            insert_row = course.insert()
            if insert_row == 1:
                return course,201
        except IntegrityError ,e:
            #insert duplicate primary_key entry
            if e[0] == 1062:
                return {'primary error': e[1]},400
        except Exception,e:
            return {'error': e[1]},400

class CourseResource(Resource):
    def get(self, cid):
        """
        获取一指定cid数据,Course表主键为cid
        """
        data = Course.get({'cid':cid})
        if data is not None:
            return data,200
        else:
            return {'error': "has no course data with cid: %s" % cid},404

    def put(self, cid):
        """
        用于修改cid对应的数据行, 表单只需填写需要修改的数据项即可
        """
        parser = reqparse.RequestParser()
        parser.add_argument('cid', type=str)
        parser.add_argument('cname', type=str)
        parser.add_argument('chours', type=int)
        parser.add_argument('credit', type=float)
        parser.add_argument('precid', type=str)
        args = parser.parse_args()
        ModifyCourse = Course.get({'cid': cid})
        #判断是否存在数据
        if ModifyCourse is None:
            return {'error' : "has no course data with cid: %s for modify(put), please send post request to create first" % cid}, 404
        #若表单给出cid,此cid与url对应不同报错
        if args['cid'] is not None and args['cid'] != cid:
            return {'error' : "url's(put) cid(%s) is not equal to form cid(%s)" % (cid, args['cid'])},400
        for key, value in args.iteritems():
            if value is not None:
                ModifyCourse[key] = value
        try:
            update_row = ModifyCourse.update()
            if update_row == 1:
                return ModifyCourse,201
        except Exception,e:
            return {'error', e[1]},400

    def delete(self, cid):
        """
        删除cid对应数据行
        """
        OldCourse = Course.get({'cid':cid})
        #判断是否有sid对应数据
        if OldCourse is None:
            return {'error': "has no course data with cid:%s for deleted" % cid},404
        try:
            delete_row = OldCourse.delete()
            if delete_row == 1:
                return { 'success' : 'success delete data with cid:%s' % cid},204
        except IntegrityError,e:
            if e[0] == 1451:
                return {'foreign error':e[1]},400 #外键约束
            return {'error':e[1]},400
        except Exception,e:
            return {'error':e[1]},400

class EmployAdd(Resource):
    """
    获取所有数据或者新增一数据.
    curl http://localhost:port/employs
    """
    def get(self):
        """
        返回列表
        """
        datas =  Employ.find_all()
        #判断是否为空
        if datas != []:
            return datas,200
        else:
            return {'error': "has no student data"},404

    def post(self):
        """
        新增数据
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sid', type=int)
        parser.add_argument('cid', type=str)
        parser.add_argument('garde', type=int)
        args = parser.parse_args()
        #判断输入完整性
        for key,value in args.iteritems():
            if value is None:
                return {'error': "Please input field: %s" % key },400
        employ = Employ(**args)
        try:
            insert_row = employ.insert()
            print insert_row
            #判断是否插入成功
            if insert_row == 1:
                return employ,201
        except  IntegrityError ,e:
            #insert duplicate primary_key entry
            if e[0] == 1062:
                return {'primary error': e[1]},400
            #外键约束
            if e[0] == 1452:
                return {'foreign error': e[1]},400
            return {'error': e[1]},400
        except Exception,e:
            return {'error': e[1]},400

class EmployResource(Resource):
    """
    查询/修改/删除一数据.
    curl http://localhost:port/employ/sid
    curl http://localhost:port/employ/cid
    curl http://localhost:port/employ/sid/cid
    """
    def get(self, sid=None, cid=None):
        """
        获取一指定sid/cid数据
        """
        #'usage': 'curl http://localhost:port/employ/sid/cid'指定sidcid返回单独一数据
        if sid is not None and cid is not None:
            data = Employ.get({'sid':sid, 'cid':cid})
            if data is not None:
                return data,200
            else:
                return {'error': "has no employ data with sid:%s and cid:%s" % (sid, cid)},404
        #'usage': 'curl http://localhost:port/employ/sid'指定sid,返回list
        elif sid is not None and cid is None:
            data = Employ.find_by('where sid="%s"' % sid)
            if data != []:
                return data,200
            else:
                return {'error': "has no employ data with sid: %s" % sid},404
        #'usage': 'curl http://localhost:port/employ/cid'指定cid,返回list
        elif sid is None and cid is not None:
            data = Employ.find_by('where cid="%s"' % cid)
            if data != []:
                return data,200
            else:
                return {'error': "has no employ data with cid: %s" % cid},404

    def put(self, sid=None, cid=None):
        """
        用于修改sid cid对应的数据行, 表单只需填写需要修改的数据项即可
        """
        if sid is None or cid is None:
            return {'usage': "curl http://localhost:port/employ/sid/cid. Please input sid and cid both."},400
        parser = reqparse.RequestParser()
        parser.add_argument('sid', type=int)
        parser.add_argument('cid', type=str)
        parser.add_argument('garde', type=int)
        args = parser.parse_args()
        ModifyEmploy = Employ.get({'sid': sid, 'cid': cid})
        #判断是否存在数据
        if ModifyEmploy is None:
            return {'error' : "has no employ data with sid:%s and cid:%s for modify(put), please send post request to create first" % (sid, cid)},404
        #若表单给出sid/cid,此sid/cid与url对应不同,报错
        if args['sid'] is not None and args['sid'] != sid:
            return {'error' : "url's(put) sid(%s) is not equal to form sid(%s)" % (sid, args['sid'])},400
        if args['cid'] is not None and args['cid'] != cid:
            return {'error' : "url's(put) cid(%s) is not equal to form cid(%s)" % (cid, args['cid'])},400
        for key, value in args.iteritems():
            if value is not None:
                ModifyEmploy[key] = value
        try:
            update_row = ModifyEmploy.update()
            if update_row == 1:
                return ModifyEmploy,201
        except Exception,e:
            return {'error', e[1]},400

    def delete(self, sid=None, cid=None):
        """
        删除sid对应数据行
        """
        if sid is None or cid is None:
            return {'usage': "curl http://localhost:port/employ/sid/cid. Please input sid and cid both."},400
        OldEmploy = Employ.get({'sid':sid, 'cid':cid})
        #判断是否有sid对应数据
        if OldEmploy is None:
            return {'error': "has no employ data with sid:%s and cid:%s for deleted" % (sid, cid)}, 404
        try:
            delete_row = OldEmploy.delete()
            if delete_row == 1:
                return {'success': "success delete data with sid:%s and cid:%s" % (sid, cid)}, 204
        except Exception,e:
            return {'error':e[1]},400


api.add_resource(StudentAdd, '/api/students')
api.add_resource(StudentResource, '/api/student/<int:sid>')
api.add_resource(CourseAdd, '/api/courses')
api.add_resource(CourseResource, '/api/course/<string:cid>')
api.add_resource(EmployAdd, '/api/employs')
api.add_resource(EmployResource, '/api/employ/<int:sid>/<string:cid>', '/api/employ/<int:sid>', '/api/employ/<string:cid>')

if __name__ == '__main__':
    with db.connection():
        app.run(host='0.0.0.0')




