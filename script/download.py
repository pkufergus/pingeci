# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
本文件提供了命令行工具的入口逻辑。

Authors: caosong(caosong@baidu.com)
Date:    2019/01/22 15:22:29
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


__all__ = [
    'main',
]
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")
sys.path.append(".")

from util.util import log
# reload(sys)
# sys.path.append("../")
sys.path.append("..")
# sys.path.append("/home/test/src/github.com/pingeci")
from service import downloadmusic

def run():
    root_dir = "/home/work/caosong/data/music/"
    filename = "{}/taglist.txt".format(root_dir)
    dl = downloadmusic.DownloadMusic()
    dl.limit = 100
    dl.root_dir = "{}/tag_20180315".format(root_dir)
    dl.data_dir = "{}/artist".format(root_dir)
    with open(filename, 'r') as f:
        i = 0
        for line in f.readlines():
            arr = line.split("\t")
            if len(arr) < 2:
                continue
            cate = arr[0].strip()
            tag = arr[1].strip()
            # tag = tag.replace("/", "_")
            # tag = tag.replace("&", "_")
            # tag = tag.replace(" ", "_")
            # if tag == "清晨":
            #     continue
            dl.get_playlist(cate, tag)
            # break

def download_artist():
    root_dir = "/home/test/data/music/artist"
    filename = "{}/artist.txt".format(root_dir)
    dl = downloadmusic.DownloadMusic()
    dl.limit = 10
    dl.root_dir = root_dir
    dl.get_artist()



if __name__ == '__main__':
    #run()
    download_artist()
    # dl.get_catlist()

    #dl.get_playlist(2, "清晨")
    # break