#!/usr/bin/env python
# -*- coding:utf-8 -*-
from util.util import log
import commands
import json

from model.struct import Music

dict_file = "/home/test/data/music/all.json"
class SearchSrv():

    def __init__(self, q=""):

        pass


    def do(self, q):
        songs = []
        cmd = "ag --nonumbers '{}' {}|head -n 2000".format(q, dict_file)
        log.info("cmd={}".format(cmd))
        (status, output) = commands.getstatusoutput(cmd)
        # print status, output
        for line in output.split("\n"):
            log.info("line={}".format(line))
            if len(line) < 10:
                continue
            song_dict = json.loads(line.strip())

            song = Music().from_dict(song_dict)
            if len(song.lyric) < 10 or len(song.id) < 1 or len(song.name) < 1:
                log.debug("filter song={}".format(line))
                continue

            #highlight
            song.highlight(q)
            songs.append(song)
            if len(songs) > 20:
                break

            # print("song={}".format(song.to_dict()))

        return songs
        pass