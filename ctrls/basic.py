# -*- coding: UTF-8 -*-

import os

import sys, time
import functools
import importlib
import threading

import tornado

try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3

try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3

try:
    from httplib import responses  # py2
except ImportError:
    from http.client import responses  # py3

try:
    responses[429]
except KeyError:
    responses[429] = 'Too Many Requests'

from lib.cache import Cache
from lib.mailx import Mailx
from lib.utils import Utils

class BasicCtrl(tornado.web.RequestHandler):
    def initialize(self):
        self._caches = {'model': {}, 'datum': {}}

    def set_default_headers(self):
        self.set_header('server', self.settings['servs'])
        self.set_header('x-frame-options', 'SAMEORIGIN')
        self.set_header('x-xss-protection', '1; mode=block')
        self.set_header('cache-control', 'no-transform')

    def head(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def write_error(self, status_code, **kwargs):
        if not self.settings['error']:
            self.flash(0, {'sta': status_code})
            return
        return super(BasicCtrl, self).write_error(*[status_code], **kwargs)

    def get_runtime_conf(self, name):
        return self.datum('confs').obtain(name)

    def get_current_user(self):
        usid = self.get_cookie("_usid")
        auid = self.get_secure_cookie('_auid')
        auth = self.get_secure_cookie('_auth')
        if usid and auth:
            user = self.datum('users').get_user_by_id(usid)
            if user and user['user_auid'] == auid and \
                    self.model('admin').generate_authword(user['user_atms'], user['user_salt']) == auth:
                return user

    def set_current_sess(self, user, days = 30):
        self.set_cookie("_usid", str(user['user_id']),
                expires_days=days)
        self.set_secure_cookie("_auid", str(user['user_auid']),
                expires_days=days, httponly = True)
        self.set_secure_cookie("_auth", self.model('admin').generate_authword(user['user_atms'], user['user_salt']),
                expires_days=days, httponly = True)

    def del_current_sess(self):
        self.clear_cookie("_auid")
        self.clear_cookie("_auth")

    def find_accept(self, name):
        return 'Accept' in self.request.headers and self.request.headers['Accept'].find(name) >= 0

    def merge_query(self, args, dels = None):
        if dels is None:
            dels = []

        for k in self.request.arguments.keys():
            if k not in args and k[0] != '_':
                args[k] = self.get_argument(k)
        for k in dels:
            if k in args:
                del args[k]
        return args

    def get_escaper(self):
        return tornado.escape

    def param_xsrfs(self):
        return '_xsrf=' + self.get_escaper().url_escape(self.xsrf_token)

    def human_valid(self):
        field = '_code'
        value = self.get_secure_cookie(field)
        if value:
            self.clear_cookie(field)
            input = self.input(field, None)
            if input:
                value = self.jsons(value)
                return 'time' in value and 'code' in value\
                        and 0 < self.stime() - value['time'] < 60\
                        and value['code'] == self.utils().str_md5_hex(\
                        self.utils().str_md5_hex(self.settings['cookie_secret']) + input.lower() + str(value['time']))
        return False

    def asset(self, name, host = '/', base = 'www', path = 'assets', vers = True):
        addr = path + "/" + name

        if self.settings['debug']:
            orig = addr.replace('.min.', '.')
            if orig != addr and os.path.exists(os.path.join(self.settings['root_path'], base, orig)):
                addr = orig

        addr = "www/{}".format(addr)
        print("addr={}".format(addr))
        if vers:
            if isinstance(vers, bool):
                vers = tornado.web.StaticFileHandler.get_version({'static_path': ''}, os.path.join(self.settings['root_path'],addr))
            if vers:
                return '%s?%s' % (os.path.join(host, addr), vers)
        return os.path.join(host, addr)

    def jsons(self, json):
        if json is None or json == '':
            return None
        return self.get_escaper().json_decode(json)

    def cache(self):
        return Cache

    def utils(self):
        return Utils

    def timer(self):
        return time

    def stime(self):
        return int(time.time())

    def ualog(self, user, text, data = ''):
        if user:
            self.datum('alogs').log(text, alog_data = data, user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
        else:
            self.datum('alogs').log(text, alog_data = data, user_ip = self.request.remote_ip)

    def tourl(self, args, base = None):
        if base == None:
            base = self.request.path
        return tornado.httputil.url_concat(base, args)

    def input(self, *args, **kwargs):
        return self.get_argument(*args, **kwargs)

    def email(self, *args, **kwargs):
        conf = self.jsons(self.get_runtime_conf('mailx'))
        if conf and 'smtp_able' in conf and conf['smtp_able']:
            threading.Thread(target=Mailx(conf).send, args = args, kwargs = kwargs).start()

    def entry(self, sign, size = 1, life = 10, swap = False):
        sign = 'entry@' + sign
        data = self.cache().obtain(sign)
        if swap or not data:
            self.cache().upsert(sign, size, life)
        return data

    def flash(self, isok, resp = None, _ext = ''):
        if resp is None:
            resp = {}

        if isok:
            resp['err'] = 0
        else:
            resp['err'] = 1

        if 'sta' in resp and resp['sta']:
            self.set_status(resp['sta'])
        else:
            resp['sta'] = self.get_status()

        if 'msg' not in resp:
            resp['msg'] = self._reason
        if 'url' not in resp:
            resp['url'] = ''
        if 'dat' not in resp:
            resp['dat'] = {}

        if _ext == '.json' or self.find_accept('json'):
            self.write(self.get_escaper().json_encode(resp))
        else:
            self.render('flash.html', resp = resp)

    def datum(self, name):
        # base = sys._getframe().f_code.co_name
        base = 'datum'
        clsn = '_'.join([v.title() for v in name.split('.')]) + base.title()
        print("clsn={} name={}".format(clsn,name))
        if clsn not in self._caches[base]:
            modn = base + '.' + name
            if modn not in sys.modules:
                # __import__(modn)
                importlib.import_module(modn)
            self._caches[base][clsn] = getattr(sys.modules[modn], clsn)({'path': self.settings['database_path']})
        return self._caches[base][clsn]

    def model(self, name):
        # base = sys._getframe().f_code.co_name
        base = 'model'
        clsn = '_'.join([v.title() for v in name.split('.')]) + base.title()
        if clsn not in self._caches[base]:
            modn = 'app.' + base + '.' + name
            if modn not in sys.modules:
                # __import__(modn)
                importlib.import_module(modn)
            self._caches[base][clsn] = getattr(sys.modules[modn], clsn)()
        return self._caches[base][clsn]

def login(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.find_accept('json'):
                self.flash(0, {'sta': 403, 'url': self.get_login_url()})
                return

            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                        if next_url.find('/index.py') == 0:
                            next_url = next_url.replace('/index.py', '', 1)

                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            self.flash(0, {'sta': 403})
            return
        return method(self, *args, **kwargs)
    return wrapper
