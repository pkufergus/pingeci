# -*- coding: UTF-8 -*-

from lib.datum import Datum
from model import dbops

class PostsDatum(Datum):
    def get_post_by_id(self, post_id):
        return self.record('select * from posts where post_id = ?', (post_id, ))

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
