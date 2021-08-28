# -*- coding: UTF-8 -*-

from lib.datum import Datum
from util.util import log
from struct import *

class UsersDatum(Datum):
    def get_user_by_id(self, user_id):
        ret = self.record('select * from artist where id = {} limit 1'.format(user_id))
        log.debug("ret={}".format(ret))
        user = {}
        if not ret:
            return user
        row = ret[0]
        user["user_id"] = row[0]
        user["user_name"] = row[2]
        user["post_ids"] = row[3]
        return user

    def get_user_by_name(self, name):
        return self.record('select * from users where user_name = ?', (name,))

    def get_user_by_mail(self, mail):
        return self.record('select * from users where user_mail = ?', (mail,))

