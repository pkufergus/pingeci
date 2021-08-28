# -*- coding: UTF-8 -*-

from basic import BasicCtrl

class LinksCtrl(BasicCtrl):
    def get(self):
        links = self.datum('links').result(
                'select link_id, link_name, link_href, link_desp, link_rank from links where link_rank>0 order by link_rank desc, link_id desc')
        print("links={}".format(links))
        rets = []
        for link in links:
            ret = {}
            ret["link_name"] = link[1]
            ret["link_href"] = link[2]
            ret["link_desp"] = link[3]
            rets.append(ret)

        self.render('links.html', links = rets)
