
from util.util import *
from struct import *

from db import *

def get_song(songid, flag = False):
    sql = """
    select netid, name, artists, lyric 
    from song
    where netid='{}'
    """.format(songid)
    log.info("sql={}".format(sql))
    results = onlinedb.query(sql)
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
    results = onlinedb.query(sql)
    if len(results) < 1:
        return ""
    row = results[0]
    netid=row[0]
    name=row[1]
    songs=row[2]
    return name, songs

def get_artist_songs(aid):
    name, songids = get_artist(aid)
    sids = songids.split(";")
    songs = []
    for sid in sids:
        song = get_song(sid)
        songs.append(song)
    return songs