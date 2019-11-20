# -*- coding: UTF-8 -*-
import json
import os
from datetime import date,datetime
import MySQLdb
from util.util import log
import re

class Artist():
    def __init__(self, id="", name=""):
        self.id = id
        self.name = name
        pass

    def to_dict(self):
        obj_dict = {
            "id":self.id,
            "name":self.name,
        }
        return obj_dict

    def from_dict(self, a_dict):
        self.id = a_dict.get("id", "")
        self.name = a_dict.get("name", "")
        return self


class Playlist():
    def __init__(self, id="", name="", tag=""):
        self.id = id
        self.name = name
        self.tag = tag
        self.root_dir = ""
        pass

    # def __init__(self):
    #     self.id = ""
    #     self.name = ""
    #     self.tag = ""
    #     self.root_dir = ""
    #     pass

    def to_dict(self):
        obj_dict = {
            "id":self.id,
            "name":self.name,
            "tag":self.tag,
        }
        return obj_dict

from db import mydb

class Music():
    def __init__(self, id="", name="", tag="", playlist=Playlist()):
        self.id = id
        self.name = name
        self.tag = [tag]
        self.playlist = playlist
        self.artists = []
        self.lyric = ""
        self.data_dir = ""
        self.lyric_highlight = ""
        pass

    # def __init__(self, id, name):
    #     self.id = id
    #     self.name = name
    #     self.tag = ""
    #     self.playlist = Playlist()
    #     self.artists = []
    #     self.lyric = ""
    #     self.data_dir = ""
    #     pass

    def save_db(self):
        print("save db")
        log.debug("save db id={}".format(self.id))
        # dblock.acquire()
        aids = [str(x.id) for x in self.artists]
        if len(aids) > 30:
            log.warn("music id={} aids to long={}".format(self.id, aids))
            aids = aids[:30]
        log.debug("save db id={}".format(self.id))

        if aids:
            aids_str = ";".join(aids)
        else:
            aids_str = ""
        log.debug("save db id={}".format(self.id))
        # if self.lyric.find("'") >= 0:
        #     self.lyric.replace("'", "\'")
        if len(self.lyric) > 1500:
            log.warn("music id={} lyric too long={}".format(self.id, self.lyric))
            self.lyric = self.lyric[:1500]
        log.debug("save db id={}".format(self.id))
        sql = """replace into song(id, netid, name, artists, tag, lyric) values('{}', '{}', '{}', '{}', '{}', '{}') """.\
            format(self.id, self.id, MySQLdb.escape_string(self.name), aids_str, self.tag, MySQLdb.escape_string(self.lyric[:1500]))
        log.info("sql={}".format(sql))
        mydb.exec_write(sql)
        log.debug("save db id={}".format(self.id))
        for a in self.artists:
            log.debug("a id={}".format(a.id))
            self.save_artist(a)
            log.debug("write id={}".format(self.id))
        # dblock.release()
        log.debug("save db id={}".format(self.id))
        pass

    def save_artist(self, artist):
        aid = artist.id
        aname = artist.name
        print("aid={}".format(aid))
        sql = """select * from artist where netid='{}' """.format(aid)
        log.info("sql={}".format(sql))
        log.info("song id={} in artists={}".format(self.id, aid))
        results = mydb.query(sql)
        print("aid={} results=len={}".format(aid, len(results)))
        songs = ""
        log.info("song id={} in artists={} song={}".format(self.id, aid, songs))
        sids = []
        for row in results:
            netid = row[1]
            name = row[2]
            songs = row[3]
            if len(songs) > 0:
                sids = songs.split(";")
                print("songs={} sid={} id={}".format(songs, sids, self.id))
                if self.id in set(sids):
                    print("song id={} in artists={}".format(self.id, aid))
                    return
                else:
                    sids.append(self.id)
                    print("songs={} sid={} id={}".format(songs, sids, self.id))
        print("songs={}, id={}".format(songs, self.id))
        if len(sids) > 200:
            log.warn("aid={} songs too long={}".format(aid, sids))
            sids = sids[:200]
        songs = ";".join(sids)
        if len(songs) < 1:
            songs = self.id
            log.info("song id={} in artists={}".format(self.id, aid))
        sql = """replace into artist(id, netid, name, songs) values('{}', '{}', '{}', '{}') """. \
            format(aid, aid, MySQLdb.escape_string(aname), songs)
        log.info("sql={}".format(sql))
        mydb.exec_write(sql)
        log.info("write a={} id={}".format(aid, self.id))
        print("write a={} id={}".format(aid, self.id))


    def to_dict(self):
        obj_dict = {
            "id":self.id,
            "name":self.name,
            "lyric":self.lyric,
            "lyric_highlight":self.lyric_highlight,
            "tag":self.tag,
            "playlist":self.playlist.to_dict(),
            "artists":[x.to_dict() for x in self.artists],
        }
        return obj_dict

    def from_dict(self, song_dict):
        self.id = song_dict.get("id", "")
        self.name = song_dict.get("name", "")
        self.lyric = song_dict.get("lyric" "")
        self.tag = song_dict.get("tag", "")
        self.artists = [Artist().from_dict(a) for a in song_dict.get("artists", [])]
        return self

    def highlight(self, q):
        p = re.compile(r"\[[0-9][0-9]:[0-9][0-9]\..{1,5}\]")
        self.lyric_highlight = p.sub("", self.lyric)
        # print("hl={}".format(self.lyric_highlight))
        p2 = re.compile(r'\n')
        y = p2.sub(" ", self.lyric_highlight)
        # print("hl2={}".format(y))
        # print("q={}".format(q))
        self.lyric_highlight = y.replace("{}".format(q), "[hight_light_start]{}[hight_light_end]".format(q))
        print("hl3={}".format(self.lyric_highlight))
