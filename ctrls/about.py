# -*- coding: UTF-8 -*-

from basic import BasicCtrl

class AboutCtrl(BasicCtrl):
    def get(self, *args):
        self.render('about.html')
