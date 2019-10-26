# -*- coding: UTF-8 -*-
################################################################################
#
#
################################################################################

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
    root_dir = "/home/work/data/music/"
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
    print("download success")
    log.info("download success")

def download_top_artist():
    root_dir = "/home/test/data/music/artist"
    filename = "{}/artist.txt".format(root_dir)
    dl = downloadmusic.DownloadMusic()
    dl.limit = 10
    dl.root_dir = root_dir
    dl.get_top_artist()
    print("download success")
    log.info("download success")
    pass

def download_top_song():
    root_dir = "/home/test/data/music/artist"
    dl = downloadmusic.DownloadMusic()
    dl.root_dir = root_dir
    dl.download_top_list()
    print("download song success")
    log.info("download song success")
    pass

import time

if __name__ == '__main__':
    #run()
    if len(sys.argv) < 2:
        exit()
    cmd = sys.argv[1]
    if cmd == "down":
        download_artist()
    elif cmd == "top_artist":
        download_top_artist()
    elif cmd == "top_song":
        download_top_song()

    # time.sleep(1000)
    # dl.get_catlist()

    #dl.get_playlist(2, "清晨")
    # break