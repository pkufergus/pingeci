# -*- coding: UTF-8 -*-

from lib.datum import Datum

class PostsDatum(Datum):
    def get_post_by_id(self, post_id):
        return self.record('select * from posts where post_id = ?', (post_id, ))

