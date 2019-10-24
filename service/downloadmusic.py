# -*- coding: UTF-8 -*-
import json
import os
from datetime import date,datetime
from tomorrow import threads
import MySQLdb
vid_map={}

from util.util import log


import tornado.ioloop
import tornado.web
import urllib
import traceback
import requests
import json
import time
import urllib

import threading
lock=threading.Lock()

dblock=threading.Lock()
import sys

from model.struct import *
from model import dbops


class DownloadMusic():
    server = "http://yq01-ps-7-m12-wise080.yq01.baidu.com:8002"
    server = "http://yq01-bdl-bdl126.yq01.baidu.com:8310"
    # root_dir = "/home/work/data/music"
    def __init__(self):
        self.g_index = 0
        self.thread_num = 0
        self.limit = 100
        self.song_limit = 500
        self.id_map = {}
        self.root_dir = "/home/test/data/music/artist"
        self.data_dir = self.root_dir
        #self.load()
        pass

    def load(self):
        filename="/home/work/caosong/data/meta/all_music.list"
        with open(filename, 'r') as f:
            i = 0
            for line in f.readlines():
                id=line.strip()
                self.id_map[id] = 1
        print("id map size={}".format(len(self.id_map)))


    def get_catlist(self):
        uri = "{}/playlist/catlist".format(self.server)

        try:
            resp = requests.get(uri)
            response = resp.json()
            print response
        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None
        f = open('{}/taglist.txt'.format(self.root_dir), 'w')
        if "sub" in response:
            for tag in response["sub"]:
                print tag["name"]
                tag_name = tag["name"]
                category = tag["category"]
                print("category={} cate_name={}".format(category, tag_name))
                f.write("{}\t{}\n".format(category, tag_name))
        f.close()

    def special_char(self, s):
        if s.find(" ") >= 0 or s.find("/") >= 0 or s.find("&") >= 0:
            return urllib.quote(s, safe="#")
        return s

    def get_playlist(self, cate, tag):
        print("tag={}".format(tag))
        tag1 = self.special_char(tag)
        print("tag1={}".format(tag1))
        tag_dir = "{}/{}/{}".format(self.root_dir, cate, tag1)
        if os.path.exists(tag_dir):
            log.info("{} exist, return".format(tag_dir))
        cmd = "mkdir -p {}".format(tag_dir)
        log.info("cmd={}".format(cmd))
        os.system(cmd)
        ret_list=[]


        # tag1=urllib.quote(tag, safe="#")
        tag1 = self.special_char(tag)

        uri = "{}/top/playlist?limit={}&order=new&cat={}".format(self.server, self.limit, tag1)
        try:
            resp = requests.get(uri)
            response = resp.json()
            print response
            if "playlists" in response:
                ret_list += response["playlists"]

        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None

        uri = "{}/top/playlist?limit={}&order=hot&cat={}".format(self.server, self.limit, tag)
        try:
            resp = requests.get(uri)
            response = resp.json()
            print response
            if "playlists" in response:
                ret_list += response["playlists"]
        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None

        time_count = 0
        self.g_index = 0
        self.thread_num = 0
        for playlist in ret_list:
            playlist_id=playlist["id"]
            playlist_name=playlist["name"]
            pl = Playlist(playlist_id, playlist_name, tag)
            pl.root_dir = tag_dir

            print("playlist name={} id={}".format(playlist_name, playlist_id))
            log.info("playlist name={} id={}".format(playlist_name, playlist_id))

            time_count = 0
            self.g_index = 0
            self.thread_num = 0
            self.download_one_playlist(pl)
            start = time.time()
            while self.g_index < self.thread_num and time_count < 3600:
                if self.thread_num > 30:
                    if self.g_index >= self.thread_num - 3:
                        break
                    else:
                        if self.g_index >= self.thread_num - 1:
                            break

                    log.info(
                        "wait for end list id={} g_index={} thread_num={} time={}".format(playlist_id, self.g_index, self.thread_num,
                                                                                          time_count))
                    time.sleep(1)
                    time_count += 1
                end = time.time()
                log.info(
                    "wait for end list id={} g_index={} thread_num={} time={}s count={}".format(playlist_id, self.g_index, self.thread_num,
                                                                                                end - start, time_count))
                # break

            # start = time.time()
            # while self.g_index < self.thread_num and time_count < 72000:
            #     if self.thread_num > 5000:
            #         if self.g_index > self.thread_num - 100:
            #             break
            #     log.info("wait for end list g_index={} thread_num={} time={}".format(self.g_index, self.thread_num, time_count))
            #     time.sleep(1)
            #     time_count += 1
            # end = time.time()
            # log.info("wait for end list g_index={} thread_num={} time={}s count={}".format(self.g_index, self.thread_num, end - start, time_count))


    def download_one_playlist(self, playlist):
        pl_dir = "{}/{}".format(playlist.root_dir, playlist.id)
        cmd = "mkdir -p {}".format(pl_dir)
        log.info("cmd={}".format(cmd))
        os.system(cmd)

        uri = "{}/playlist/detail?id={}".format(self.server, playlist.id)

        try:
            resp = requests.get(uri)
            response = resp.json()
            print response
        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None

        if "playlist" in response and "tracks" in response["playlist"]:
            i = 0
            for track in response["playlist"]["tracks"]:
                song_id = track["id"]
                song_name = track["name"]
                m = Music(song_id, song_name, playlist.tag, playlist)
                print("music name={} id={}".format(song_name, song_id))
                self.thread_num += 1
                self.download_one_song(m)
                i += 1
                # break
                if i > self.song_limit:
                    break

    @threads(20)
    def download_one_song(self, music):
        try:
            self._download_one_song(music)
        except Exception as e:
            log.info("music={} error={}".format(music.to_dict(), e))
        finally:
            lock.acquire()
            self.g_index += 1
            lock.release()

    def _download_one_song_mp3(self, music):
        uri = "{}/music/url?id={}".format(self.server, music.id)
        try:
            resp = requests.get(uri,timeout=300)
            response = resp.json()
            # print response
        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None

        if "data" in response:
            for one_music in response["data"]:
                url = one_music["url"]
                cmd = "wget -c {} -O {}/{}.mp3 -o {}/{}.wget.log".format(url, self.data_dir, music.id, self.data_dir, music.id)
                log.info("cmd={}".format(cmd))
                os.system(cmd)
                break

    def _download_one_song(self, music):


        # music_dir = self.root_dir
        # key = "{}.mp3".format(music.id)
        # if key in self.id_map:
        #     log.info("{} name={} exist".format(key, music.name))
        #     return

        # json_file = '{}/{}.json'.format(music_dir, music.id)
        # mp3_file = '{}/{}.mp3'.format(self.data_dir, music.id)
        # if os.path.exists(json_file) and os.path.exists(mp3_file):
        #     log.info("{} name={} exist".format(json_file, music.name))
        #     return
        #
        # if os.path.exists(mp3_file):
        #     log.info("{} name={} exist".format(mp3_file, music.name))
        # else:
        #     self._download_one_song_mp3(music)

        # uri = "{}/music/url?id={}".format(self.server, music.id)
        #
        # try:
        #     resp = requests.get(uri,timeout=60)
        #     response = resp.json()
        #     print response
        # except BaseException as e:
        #     print '获取人脸信息失败!'
        #     print e
        #     return None
        #
        # if "data" in response:
        #     for one_music in response["data"]:
        #         url = one_music["url"]
        #         cmd = "wget -c {} -O {}/{}.mp3 -o {}/{}.wget.log".format(url, music_dir, music.id, music_dir, music.id)
        #         log.info("cmd={}".format(cmd))
        #         os.system(cmd)
        #         break

        uri = "{}/lyric?id={}".format(self.server, music.id)

        try:
            resp = requests.get(uri, timeout=60)
            response = resp.json()
            # print response
        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None

        if "lrc" in response and "lyric" in response["lrc"]:
            music.lyric = response["lrc"]["lyric"]
            # print("id={} lyric={}".format(music.id, music.lyric))

        uri = "{}/song/detail?ids={}".format(self.server, music.id)
        try:
            resp = requests.get(uri,timeout=60)
            response = resp.json()
            # log.info(response)
        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None

        if "songs" in response:
            for one_music in response["songs"]:
                if "ar" in one_music:
                    for a in one_music["ar"]:
                        a_id = a["id"]
                        a_name = a["name"]
                        music.artists.append(Artist(a_id, a_name))
                break
        # print("m={}".format(music.to_dict()))
        playlist = music.playlist
        if not playlist.root_dir:
            playlist.root_dir = self.root_dir
        root_dir = self.root_dir
        id_dir = ""
        if music.artists:
            id_dir = music.artists[0].id
        music_dir = "{}/{}/{}".format(root_dir, id_dir, music.id)
        cmd = "mkdir -p {}".format(music_dir)
        log.info("cmd={}".format(cmd))
        os.system(cmd)
        obj_dict = music.to_dict()
        obj_json = json.dumps(obj_dict, ensure_ascii=False)
        # print("id={} json={}".format(music.id, obj_json))
        f = open('{}/{}.json'.format(music_dir, music.id), 'w')
        f.write(obj_json)
        f.close()
        music.save_db()
        print("save {} ok!".format(music.id))


    def get_artist(self):
        cmd = "mkdir -p {}".format(self.root_dir)
        log.info("cmd={}".format(cmd))
        os.system(cmd)
        type_ids = ["1", "2", "4", "5", "6", "7"]
        prefix_artist = [x for x in range(65, 91)]
        prefix_artist.append(0)
        print("prefix={}".format(prefix_artist))
        # url = "https://music.163.com/#/discover/artist/cat?id={}&initial={}"
        url = "{}/artist/list?cat={}&limit=100"
        for type_id in type_ids[3:]:
            id_list = [type_id + x for x in ["001", "002", "003"]]
            for t_id in id_list:
                a_num = 0
                print("type id={}".format(t_id))
                uri = url.format(self.server, t_id)
                print("uri={}".format(uri))
                try:
                    resp = requests.get(uri, timeout=120)
                    response = resp.json()
                    print response
                except BaseException as e:
                    print '{}获取artist fail!'.format(uri)
                    print e
                    continue
                print("uri={}".format(uri))
                time_count = 0
                self.g_index = 0
                self.thread_num = 0
                if "artists" in response:
                    for one_artist in response["artists"]:
                        a_id = one_artist["id"]
                        a_name = one_artist["name"]
                        ar = Artist(a_id, a_name)


                        self.download_one_artist(ar)
                        a_num += 1
                        time.sleep(1)
                        # break
                start = time.time()
                # while self.g_index < self.thread_num - 1 and time_count < 3600:
                #     log.info(
                #         "wait for end list g_index={} thread_num={} time={}".format(self.g_index,
                #                                                                           self.thread_num,
                #                                                                           time_count))
                #     time.sleep(1)
                #     time_count += 1
                end = time.time()
                log.info(
                    "wait for end list g_index={} thread_num={} time={}s count={}".format(
                        self.g_index,
                        self.thread_num,
                        end - start,
                        time_count))
                # break
                log.info("down success typeid={} t_id={} a num={}".format(type_id, t_id, a_num))
                time.sleep(20)
            # break

    def download_one_artist(self, artist):
        # pl_dir = "{}/{}".format(self.root_dir, playlist.id)
        # cmd = "mkdir -p {}".format(pl_dir)
        # log.info("cmd={}".format(cmd))
        # os.system(cmd)

        uri = "{}/artists?id={}".format(self.server, artist.id)

        try:
            resp = requests.get(uri)
            response = resp.json()
            print response
        except BaseException as e:
            print '获取人脸信息失败!'
            print e
            return None

        if "hotSongs" in response:
            i = 0
            for song in response["hotSongs"]:
                song_id = str(song["id"])
                song_name = str(song["name"])
                m = Music(song_id, song_name)
                # if "ar" in song:
                #     for a in song["ar"]:
                #         a_id = a["id"]
                #         a_name = a["name"]
                #         m.artists.append(Artist(a_id, a_name))
                # print("music name={} id={}".format(song_name, song_id))
                self.thread_num += 1
                self.download_one_song(m)
                i += 1
                # break
                # if i > 3:
                #     break
        print("down artist ok id={} name={}".format(artist.id, artist.name))

    def get_douyin(self):

        url = "{}/search?keywords=抖音热歌&limit=100"
        uri = url.format(self.server)
        print("uri={}".format(uri))
        f = open('{}/douyin.txt'.format(self.root_dir), 'w')
        try:
            resp = requests.get(uri, timeout=120)
            response = resp.json()
            print response
        except BaseException as e:
            print '{}获取artist fail!'.format(uri)
            print e
            return
        if "result" in response and "songs" in response["result"]:
            for song in response["result"]["songs"]:
                id = song["id"]
                name = song["name"]
                f.write("{}\t{}\n".format(id, name))
                if "{}.mp3".format(id) in self.id_map:
                    log.info("id={} name={} exist".format(id, name))
                else:
                    json_file = '{}/{}.json'.format(self.root_dir, id)
                    if os.path.exists(json_file):
                        log.info("id={} name={} exist".format(id, name))
                    else:
                        log.info("id={} name={} not_exist".format(id, name))

        f.close()

    def get_top_artist(self):
        cmd = "mkdir -p {}".format(self.root_dir)
        log.info("cmd={}".format(cmd))
        os.system(cmd)
        url = "{}/top/artists".format(self.server)
        a_num = 0
        try:
            resp = requests.get(url, timeout=120)
            response = resp.json()
            # response
        except BaseException as e:
            print '{}获取artist fail!'.format(url)
            log.fatal("err={} url={}".format(e, url))
            print e
            print("uri={}".format(url))
        artist_list = []
        if "artists" in response:
            for one_artist in response["artists"]:
                a_id = str(one_artist["id"]).strip()
                a_name = str(one_artist["name"]).strip()
                ar = Artist(a_id, a_name)
                artist_list.append(ar)
                self.download_one_artist(ar)
                a_num += 1
                time.sleep(1)
        print("down ok a_num={}".format(a_num))
        log.info("down ok a_num={}".format(a_num))
        if len(artist_list) < 1:
            log.fatal("too few top artists len={}".format(len(artist_list)))
            return
        log.info("write artist into top list")
        ar_str_list = [str(a.id) + "$$" + str(a.name) for a in artist_list]
        ar_str_list_str = ";".join(ar_str_list)
        dbops.write_top_artist(ar_str_list_str)
        log.info('write artist into top list success')


if __name__ == '__main__':
    dl = DownloadMusic()
    #dl.get_catlist()

    # dl.get_playlist(2, "清晨")
    dl.download_one_artist(Artist('840134','刘瑞琦'))
