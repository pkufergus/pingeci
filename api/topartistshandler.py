#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado import httpclient
from tornado.web import asynchronous
from tornado import gen
import json
from model import dbops

class TopArtistsHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        ret = {}
        ret['errcode'] = 0
        ret['errmsg'] = ""
        artists = dbops.get_top_artist()
        if artists is None:
            ret['errcode'] = 1
            ret['errmsg'] = 'not find top artist'
            self.write(json.dumps(ret, ensure_ascii=False))
            return
        ret['data'] = [a.to_dict() for a in artists]
        self.write(json.dumps(ret, ensure_ascii=False))