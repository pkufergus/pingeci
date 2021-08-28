#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado import httpclient
from tornado.web import asynchronous
from tornado import gen
import json
from model import dbops

class ArtistHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        aid = self.get_argument("artistid", "")
        ret = {}
        ret['errcode'] = 0
        ret['errmsg'] = ""
        if not aid or len(aid) < 2:
            ret['errcode'] = 1
            ret['errmsg'] = 'no artist'
            self.write(json.dumps(ret, ensure_ascii=False))
            return

        aid = aid[:20]
        songs = dbops.get_artist_songs(aid)
        if songs is None:
            ret['errcode'] = 1
            ret['errmsg'] = 'not find artist id={}'.format(aid)
            self.write(json.dumps(ret, ensure_ascii=False))
            return
        ret['data'] = [song.to_dict() for song in songs]
        self.write(json.dumps(ret, ensure_ascii=False))