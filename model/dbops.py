
from util.util import *
from struct import *

from mysqlpool import *
import MySQLdb

import re

def get_song(songid, flag = False):
    sql = """
    select netid, name, artists, lyric 
    from song
    where netid='{}'
    """.format(songid)
    log.info("sql={}".format(sql))
    results = mypool.query(sql)
    if len(results) < 1:
        return None
    row = results[0]
    netid = row[0]
    name = row[1]
    artists = row[2]
    lyric = row[3]
    aid = ""
    aname = ""
    if len(artists) > 0 and flag:
        aid = artists.split(";")[0]
        aname, _ = get_artist(aid)
    a = Artist(aid, aname)
    song = Music(songid, name)
    song.lyric = lyric
    song.artists.append(a)
    return song


def get_artist(aid):
    sql = """
        select netid, name, songs 
        from artist
        where netid='{}'
        """.format(aid)
    log.info("sql={}".format(sql))
    results = mypool.query(sql)
    if len(results) < 1:
        return ""
    row = results[0]
    netid=row[0]
    name=row[1]
    songs=row[2]
    return name, songs

def get_artist_songs(aid, limit = 1000):
    name, songids = get_artist(aid)
    sids = songids.split(";")
    songs = []
    for sid in sids[:limit]:
        song = get_song(sid)
        songs.append(song)
    return songs

def get_artist_songs_from_ids(songids, limit = 1000):
    sids = songids.split(";")
    songs = []
    for sid in sids[:limit]:
        song = get_song(sid)
        songs.append(song)
    return songs

def write_top_artist(ar_list_str):
    sql = """
        replace into kv(keyid, value)
        values('{}', '{}')
    """.format("top_artists", MySQLdb.escape_string(ar_list_str))
    log.debug("sql = {}".format(sql))
    mypool.exec_write(sql)
    log.debug("save db ok arlist={}".format(ar_list_str))

def get_top_artist(limit=50):
    sql = """
        select keyid, value
        from kv
        where keyid='{}'
    """.format('top_artists')
    log.debug("sql = {}".format(sql))
    results = mypool.query(sql)
    artists = []
    if len(results) < 1:
        return artists
    row = results[0]
    log.info("row={}".format(row))
    keyid = str(row[0])
    log.info("row[1]={}".format(row[1]))
    value = row[1]
    ar_str_list = value.split(";")
    log.info("ar_str_list={}".format(ar_str_list))
    for ar_str in ar_str_list:
        aid, aname = str(ar_str).split("$$")
        artists.append(Artist(aid, aname))
    return artists[:limit]


def write_top_song(song_list_str):
    sql = """
        replace into kv(keyid, value)
        values('{}', '{}')
    """.format("top_songs", MySQLdb.escape_string(song_list_str[:12000]))
    log.debug("sql = {}".format(sql))
    mypool.exec_write(sql)
    log.debug("save db ok song={}".format(song_list_str))

def get_top_songs(limit=20):
    songs = []
    if limit < 1 or limit > 200:
        log.fatal("err=limit error")
        return songs
    sql = """
        select keyid, value
        from kv
        where keyid='{}'
    """.format('top_songs')
    log.debug("sql = {}".format(sql))
    results = mypool.query(sql)
    if len(results) < 1:
        return songs
    row = results[0]
    log.info("row={}".format(row))
    keyid = str(row[0])
    log.info("row[1]={}".format(row[1]))
    value = row[1]
    song_str_list = value.split(";")
    log.info("top_songs={}".format(song_str_list))
    ids = []
    for song_str in song_str_list:
        id, name = str(song_str).split("$$")
        id = "'{}'".format(id)
        ids.append(id)
    sql = """
            select netid, lyric
            from song
            where netid in ({})
        """.format(",".join(ids))
    log.debug("sql = {}".format(sql))
    results = mypool.query(sql)
    metas = {}
    for result in results:
        id, lyric = result[0], result[1]
        metas[id] = lyric
    for song_str in song_str_list:
        id, name = str(song_str).split("$$")
        m = Music(id, name)
        m.lyric = metas[id]
        m.lyric = re.sub(r'\[[0-9:.]*\]', "", m.lyric)
        songs.append(m)
    return songs[:limit]