#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado import httpclient
from tornado.web import asynchronous
from tornado import gen
import json
from service.searchservice import SearchSrv

class SearchHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        q = self.get_argument("q", "")
        ret = {}
        ret['errcode'] = 0
        ret['errmsg'] = ""
        if not q or len(q) < 1:
            ret['errcode'] = 1
            ret['errmsg'] = 'no query'
            self.write(json.dumps(ret, ensure_ascii=False))
            return

        if len(q) > 50:
            ret['errcode'] = 2
            ret['errmsg'] = 'query too long'
            self.write(json.dumps(ret, ensure_ascii=False))
            return

        query = q.strip()[:50]
        songs = SearchSrv().do(query)
        if songs is None:
            ret['errcode'] = 3
            ret['errmsg'] = 'not find songs query={}'.format(q)
            self.write(json.dumps(ret, ensure_ascii=False))
            return
        ret['data'] = [song.to_dict() for song in songs]
        self.write(json.dumps(ret, ensure_ascii=False))