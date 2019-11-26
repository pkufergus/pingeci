# -*- coding: UTF-8 -*-

from . import shell, ShellCtrl
from model import dbops
import re

class Shell_IndexCtrl(ShellCtrl):
    def get(self, artist_id):
        stime = self.stime()
        pager = {}
        pager['qnty'] = 5
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        user = self.datum('users').get_user_by_id(artist_id)
        if not user:
            self.flash(0, {'sta': 404})
            return

        songs = dbops.get_artist_songs_from_ids(user["post_ids"], limit=50)
        posts = []
        for song in songs:
            post = {}
            post["post_id"] = song.id
            post["post_title"] = song.name
            song.lyric = re.sub(r'\[[0-9:.]*\]', "", song.lyric)
            if len(song.lyric) > 10:
                post["post_descr"] = song.lyric[:120] + "..."
            else:
                post["post_descr"] = ""
            posts.append(post)

        if posts:
            pager['lgth'] = len(posts)

        posts_top = []
        posts_new = []
        posts_rel = []
        slabs_top = []
        terms_top = []
        talks_new = []
        links_top = []
        artists_hot = self.datum('posts').get_top_artists()

        if self.input('_pjax', None) == '#shell-index-posts':
            self.render('shell/index/posts.html', user = user, pager = pager, posts = posts)
            return

        self.render('shell/index.html', user=user, pager=pager, posts=posts, posts_top=posts_top, artists_hot=artists_hot,
                    posts_new=posts_new, posts_rel=posts_rel
                    , slabs_top=slabs_top, terms_top=terms_top, talks_new=talks_new, links_top=links_top)
