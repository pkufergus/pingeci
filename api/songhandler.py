#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado import httpclient
from tornado.web import asynchronous
from tornado import gen
import json
from model import dbops

class SongHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        sid = self.get_argument("songid", "")
        ret = {}
        ret['errcode'] = 0
        ret['errmsg'] = ""
        if not sid or len(sid) < 5:
            ret['errcode'] = 1
            ret['errmsg'] = 'no songid'
            self.write(json.dumps(ret, ensure_ascii=False))
            return

        sid = sid[:20]
        song = dbops.get_song(sid, True)
        if song is None:
            ret['errcode'] = 1
            ret['errmsg'] = 'not find sid={}'.format(sid)
            self.write(json.dumps(ret, ensure_ascii=False))
            return
        ret['data'] = song.to_dict()
        self.write(json.dumps(ret, ensure_ascii=False))


    def callback(self, response):
        print response.body



class TopSongsHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        ret = {}
        ret['errcode'] = 0
        ret['errmsg'] = ""
        limit = self.get_argument("limit", "50")
        if int(limit) < 1:
            ret['errcode'] = 1
            ret['errmsg'] = 'parameter error'
            self.write(json.dumps(ret, ensure_ascii=False))
            return
        songs = dbops.get_top_songs(int(limit))
        if songs is None:
            ret['errcode'] = 1
            ret['errmsg'] = 'not find top artist'
            self.write(json.dumps(ret, ensure_ascii=False))
            return
        ret['data'] = [s.to_dict() for s in songs]
        self.write(json.dumps(ret, ensure_ascii=False))