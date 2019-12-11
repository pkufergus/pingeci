# -*- coding: UTF-8 -*-

from basic import BasicCtrl
from service.searchservice import SearchSrv

class PostsCtrl(BasicCtrl):
    def get(self, _tnm = None):
        pager = {}
        pager['qnty'] = 5
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        print("_tnm={}".format(_tnm))
        stime = self.stime()
        track = ''

        _qry = self.input('q', None)
        _top = False
        _tag = None
        posts = []
        ptids = {}
        ptags = {}
        psers = {}
        posts_top = {}
        artists_hot = []
        posts_new = []
        posts_rel = []
        slabs_top = []
        terms_top = []
        talks_new = []
        links_top = []

        if _qry:
            posts = self.datum('posts').search(_qry)
            pass
        else:
            posts = self.datum('posts').get_top_songs()
            if self.input('page', None) is None:
                _top = True

        artists_hot = self.datum('posts').get_top_artists()


        self.render('posts.html', track=track, pager=pager, posts=posts, psers=psers, ptids=ptids, ptags=ptags
                    , posts_top=posts_top, artists_hot=artists_hot, posts_new=posts_new, posts_rel=posts_rel
                    , slabs_top=slabs_top, terms_top=terms_top, talks_new=talks_new, links_top=links_top)


class PostCtrl(BasicCtrl):
    def get(self, post_id):
        stime = self.stime()
        print("post_id={}".format(post_id))

        post = self.datum('posts').get_post_by_id(post_id)
        if not post:
            self.flash(0, {'sta': 404})
            return

        ptids = {}
        ptags = {}
        psers = {}

        ptids = []
        psers = []

        post_prev = ""
        post_next = ""

        talks = None
        talks_new = None
        slabs_top = None
        links_top = None
        artists_hot = self.datum('posts').get_top_artists()
        posts_top = []
        posts_new = []
        posts_rel = []
        slabs_top = []
        terms_top = []
        talks_new = []
        links_top = []

        self.render('post.html', post = post, psers = psers, ptids = ptids, ptags = ptags, talks = talks
                , post_prev = post_prev, post_next = post_next
                , posts_top = posts_top, artists_hot=artists_hot, posts_new = posts_new, posts_rel = posts_rel
                , slabs_top = slabs_top, terms_top = terms_top, talks_new = talks_new, links_top = links_top)
