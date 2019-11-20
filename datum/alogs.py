# -*- coding: UTF-8 -*-

import time
from lib.datum import Datum

class AlogsDatum(Datum):

    def log(self, alog_text, alog_data = '', user_ip = '', user_id = 0, user_name = ''):
        self.submit('insert into alogs (user_ip, user_id, user_name, alog_text, alog_data, alog_ctms) values (?, ?, ?, ?, ?, ?)',
                (user_ip, user_id, user_name, alog_text, alog_data, int(time.time())))
