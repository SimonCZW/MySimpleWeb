#!/usr/bin/python
# -*- coding:utf-8 -*-

def application_base(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello World!</h1>'

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello %s!</h1>' % (environ['PATH_INFO'][1:])


