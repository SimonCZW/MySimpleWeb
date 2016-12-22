#!/usr/bin/python
class Sample:
    def __enter__(self):
        #print "In __enter__()"
        #return "Foo"
        return self
    def __exit__(self, type, value, trace):
        #print "In __exit__()"
        print "type:", type
        print "value:", value
        print "trace:", trace

    def do_something(self):
        bar = 1/0
        return bar + 10


with Sample() as sample:
#    print "sample:", sample
    sample.do_something()

