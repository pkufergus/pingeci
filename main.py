#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado import httpclient
from tornado.web import asynchronous
from tornado import gen

import sys

reload(sys)

sys.setdefaultencoding('utf-8')


from api.handler import MainHandler

settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'static_url_prefix': '/static/',
}

application = tornado.web.Application(
    handlers=[(r'/', MainHandler),
              ],
    **settings)

if __name__ == "__main__":
    hostname="bjhw-ps-superpage4651.bjhw.baidu.com"
    port=8330
    print("http://{}:{}".format(hostname, port))
    print("http://{}:{}/page".format(hostname, port))
    application.listen(8330)
    tornado.ioloop.IOLoop.instance().start()