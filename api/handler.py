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


class MainHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        self.render('index.html')

    def callback(self, response):
        print response.body