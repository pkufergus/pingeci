# -*- coding: UTF-8 -*-
import json
import os
from datetime import date,datetime
from tomorrow import threads
from model import stuff
from model import util

vid_map={}

from lib import log

import tornado.ioloop
import tornado.web
import urllib
import traceback
import requests
import json
import time

import threading
lock=threading.Lock()



class Video():
    def __init__(self, id):
        self.id = id

        pass

    def get_url(self):
        meta = gcmc.get_gcmc(self.id)
        print("vid={} meta={}".format(self.id, meta))
        url = ""
        return url

    def to_dict(self):
        obj_dict = {
            "id":self.id,
        }
        return obj_dict

class DownloadVideo():
    root_dir = "/home/work/test/data/video"
    def __init__(self):
        self.g_index = 0
        self.thread_num = 0
        pass

    @threads(20)
    def download_one_video(self, vid, url):
        try:
            print("vid={} url={}".format(vid, url))
            vdir = "{}/{}".format(self.root_dir, vid)
            cmd = "mkdir -p {}".format(vdir)
            log.notice("vid={} cmd={}".format(vid, cmd))
            os.system(cmd)
            cmd = "wget -c {} -O {}/{}.mp4 -o {}/{}.wget.log".format(url, vdir, vid, vdir, vid)
            log.notice("vid={} cmd={}".format(vid, cmd))
            os.system(cmd)

            wavfile = "{}/{}.wav".format(vdir, vid)
            if os.path.exists(wavfile):
                os.system("rm -f {}".format(wavfile))
            cmd = "ffmpeg -i {}/{}.mp4 -f wav -ar 16000 {}/{}.wav".format(vdir, vid, vdir, vid)
            log.notice("vid={} cmd={}".format(vid, cmd))
            os.system(cmd)
            print("vid={} url={} success".format(vid, url))
        except Exception as e:
            print("vid={} e={}".format(vid, e))
            log.fatal("vid={} e={}".format(vid, e))

        # finally:
        #     lock.acquire()
        #     self.g_index += 1
        #     lock.release()


if __name__ == '__main__':
    dv = DownloadVideo()
    #dl.get_catlist()

