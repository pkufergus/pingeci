# -*- coding: UTF-8 -*-

from basic import BasicCtrl

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

        post = self.datum('posts').get_post_by_id(post_id)
        if not post or ((not self.get_current_user()) and (not post['post_stat'] or post['post_ptms'] >= stime)):
            self.flash(0, {'sta': 404})
            return

        ptids = {}
        ptags = {}
        psers = {}

        ptids = self.datum('posts').result('select post_id,term_id from post_terms where post_id = ?', (post_id, ))
        if ptids:
            ptags = self.utils().array_keyto(self.datum('terms').result('select * from terms where term_id in (' + ','.join(str(i['term_id']) for i in ptids) + ')'), 'term_id')
        ptids = self.utils().array_group(ptids, 'post_id')
        psers = self.utils().array_keyto(self.datum('users').result('select * from users where user_id=?', (post['user_id'], )), 'user_id')

        post_prev = self.datum('posts').record(
                'select post_id from posts where post_stat>0 and post_ptms<? and post_id<? order by post_id desc limit 1', (stime, post_id, ))
        if post_prev:
            post_prev = post_prev['post_id']
        else:
            post_prev = 0

        post_next = self.datum('posts').record(
                'select post_id from posts where post_stat>0 and post_ptms<? and post_id>? order by post_id asc limit 1', (stime, post_id, ))
        if post_next:
            post_next = post_next['post_id']
        else:
            post_next = 0

        posts_top = self.datum('posts').result('select post_id,post_title,post_descr from posts where post_stat>0 and post_ptms<? and post_rank>=? order by post_rank desc, post_id desc limit 9', (stime, self.get_runtime_conf('index_posts_top_rank')))
        posts_hot = self.datum('posts').result('select post_id,post_title,post_descr from posts where post_stat>0 and post_ptms<? order by post_refc desc, post_id desc limit 9', (stime,))
        posts_new = self.datum('posts').result('select post_id,post_title,post_descr from posts where post_stat>0 and post_ptms<? order by post_ptms desc, post_id desc limit 9', (stime,))
        posts_rel = None
        if post['post_id'] in ptids:
            poids = self.datum('posts').result('select distinct post_id from post_terms where post_id<>? and term_id in (' + ','.join(str(i['term_id']) for i in ptids[post['post_id']]) + ') order by term_id desc limit 9', (post['post_id'],))
            if poids:
                posts_rel = self.datum('posts').result('select post_id,post_title,post_descr from posts where post_stat>0 and post_ptms<? and post_id in (' + ','.join(str(i['post_id']) for i in poids) + ') order by post_ptms desc, post_id desc limit 9', (stime,))

        terms_top = self.datum('terms').result('select * from terms where term_refc>0 order by term_refc desc, term_id desc limit 32')

        talks = None
        talks_new = None
        slabs_top = None
        links_top = None

        self.render('index/post.html', post = post, psers = psers, ptids = ptids, ptags = ptags, talks = talks
                , post_prev = post_prev, post_next = post_next
                , posts_top = posts_top, posts_hot = posts_hot, posts_new = posts_new, posts_rel = posts_rel
                , slabs_top = slabs_top, terms_top = terms_top, talks_new = talks_new, links_top = links_top)
