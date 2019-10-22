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
from api.songhandler import SongHandler
from api.artisthandler import ArtistHandler

settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'static_url_prefix': '/static/',
}

application = tornado.web.Application(
    handlers=[(r'/', MainHandler),
              (r'/song', SongHandler),
              (r'/artist', ArtistHandler),
              ],
    **settings)

if __name__ == "__main__":
    hostname="yq01-bdl-bdl126.yq01.baidu.com"
    port=8330
    print("http://{}:{}".format(hostname, port))
    print("http://{}:{}/page".format(hostname, port))
    print("http://{}:{}/song?songid=".format(hostname, port))
    print("http://{}:{}/artist?artistid=".format(hostname, port))
    application.listen(8330)
    tornado.ioloop.IOLoop.instance().start()