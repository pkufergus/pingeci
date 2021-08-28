#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado import httpclient
from tornado.web import asynchronous
from tornado import gen
from tornado.options import define, options

import sys

reload(sys)

sys.setdefaultencoding('utf-8')


from api.handler import MainHandler
from api.songhandler import SongHandler
from api.songhandler import TopSongsHandler
from api.searchhandler import SearchHandler
from api.artisthandler import ArtistHandler
from api.topartistshandler import TopArtistsHandler

from ctrls.posts import *
from ctrls.about import *
from ctrls.links import *
from ctrls.shell.index import *

from etc import etc


application = tornado.web.Application(
    handlers=[(r'/', PostsCtrl),
              (r'/s', PostsCtrl),
              (r'/geci/([1-9][0-9]{1,50})', PostCtrl),
              (r'/geshou/([1-9][0-9]{1,50})', Shell_IndexCtrl),
              (r'/about', AboutCtrl),
              (r'/links', LinksCtrl),
              (r'/posts', PostsCtrl),
              (r'/song', SongHandler),
              (r'/artist', ArtistHandler),
              (r'/top_artists', TopArtistsHandler),
              (r'/top_songs', TopSongsHandler),
              (r'/search', SearchHandler),
              ],
    **etc)

define("port", default=8330, help="run on the given port", type=int)
if __name__ == "__main__":
    options.parse_command_line()
    port = options.port
    hostname="10.156.102.16"
    hostname="127.0.0.1"
    print("http://{}:{}".format(hostname, port))
    print("http://{}:{}/page".format(hostname, port))
    print("http://{}:{}/song?songid=".format(hostname, port))
    print("http://{}:{}/artist?artistid=".format(hostname, port))
    print("http://{}:{}/top_artists".format(hostname, port))
    print("http://{}:{}/top_songs".format(hostname, port))
    print("http://{}:{}/search".format(hostname, port))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()