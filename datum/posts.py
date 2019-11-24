# -*- coding: UTF-8 -*-

from lib.datum import Datum
from model import dbops
import re

class PostsDatum(Datum):
    def get_post_by_id(self, post_id):
        song = dbops.get_song(post_id, True)
        post = {}
        if not song:
            return post
        post["post_title"] = song.name
        post["post_id"] = song.id
        post["post_descr"] = "歌词"
        song.lyric = re.sub(r'\[[0-9:.]*\]', "<br>", song.lyric)
        post["post_content"] = song.lyric
        if song.artists:
            post["artist_id"] = song.artists[0].id
            post["artist_name"] = song.artists[0].name
            post["post_author"] = song.artists[0].name
        return post

    def get_top_songs(self):
        songs = dbops.get_top_songs(50)
        posts = []
        for song in songs:
            post = {}
            post["post_id"] = song.id
            post["post_title"] = song.name
            post["post_summary"] = song.lyric[:120] + "..."
            posts.append(post)
        return posts

    def get_top_artists(self):
        artists = dbops.get_top_artist(50)
        rets = []
        for ar in artists:
            ret = {}
            ret["artist_id"] = ar.id
            ret["artist_name"] = ar.name
            rets.append(ret)
        return rets
