#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pyspider.libs.base_handler import *

import os
import re
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=1)
    def on_start(self):
        self.crawl('yq01-bdl-bdl126.yq01.baidu.com:8330', callback=self.index_page)

    @config(age=60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            print("save={}".format(response.save))
            ret = self.crawl(each.attr.href, callback=self.detail_page, save={"step":5})

            print("ret={}".format(ret))

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        print("url={}".format(url))
        if url.find("pingeci.com") > 0:
            return {}
        if url.startswith("http://"):
            url = url.split("http://")[1]
        if url.find("yq01-bdl-bdl126.yq01.baidu.com:8330") >= 0:
            url = url.split("yq01-bdl-bdl126.yq01.baidu.com:8330")[1]
        print("url={}".format(url))
        # if url == "/":
        #     return {}
        pos = url.find("/")
        pos_2 = url.find("?")
        if pos_2 < 0:
            pos_2 = len(url)
        filename = url[pos:pos_2]
        pos_3 = filename.rfind("/")
        dir = filename[pos:pos_3]
        dirname = "." + dir
        print("dir={}".format(dir))
        if dir == "" or dir == "/" or os.path.exists(dirname):
            pass
        else:
            os.mkdir(dirname)
        filename = "." + filename
        if filename == "./":
            filename = "index"
        print("filename={}".format(filename))
        content = response.content
        res_txt = []
        for line in content.split("\n"):
            # print("line={}".format(line))
            if line.find("href=") > 0:
                if line.find("about") > 0 or line.find("links") > 0 or line.find("/geci/") > 0 or line.find("/geshou/") > 0:
                    line_str = re.sub(r'href="([/a-z0-9]*)"', 'href="\g<1>.html"', line)
                    print("ret={}".format(line_str))
                    res_txt.append(line_str)
                else:
                    res_txt.append(line)
            else:
                res_txt.append(line)

        fp = open("{}.html".format(filename), "w")
        fp.write("\n".join(res_txt))
        fp.close()
        # print("url={} title={}".format(response.content, response.doc("html").text().encode("utf-8")))

        step = 0
        if response.save:
            step = response.save.get("step")
        print("step={}".format(step))
        step = int(step)
        if step > 0:
            for each in response.doc('a[href^="http"]').items():
                ret = self.crawl(each.attr.href, callback=self.detail_page, save={"step":step - 1})
                print("ret2={}".format(ret))
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }