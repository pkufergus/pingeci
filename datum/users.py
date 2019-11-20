# -*- coding: UTF-8 -*-

from lib.datum import Datum

class UsersDatum(Datum):
    def get_user_by_id(self, user_id):
        return self.record('select * from users where user_id = ?', (user_id,))

    def get_user_by_name(self, name):
        return self.record('select * from users where user_name = ?', (name,))

    def get_user_by_mail(self, mail):
        return self.record('select * from users where user_mail = ?', (mail,))

