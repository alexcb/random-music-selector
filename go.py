#!/usr/bin/env python3
import os
import random
import signal

from distutils.dir_util import copy_tree

ctrl_c_exit = False

def handler(signum, frame):
    global ctrl_c_exit
    ctrl_c_exit = True
    print('exiting after copy finishes')
signal.signal(signal.SIGINT, handler)

def get_albums(rootpath):
    foundalbums=[]
    artists = os.listdir(rootpath)
    for artist in artists:
        artistpath=os.path.join(rootpath, artist)
        if os.path.isdir(artistpath):
            albums = os.listdir(artistpath)
            for album in albums:
                albumpath=os.path.join(artistpath, album)
                if os.path.isdir(albumpath):
                    foundalbums.append(albumpath)
    return foundalbums

albums = get_albums('/media/nugget_share/music/alex-beet')

dst='/media/alex/TUNES'

num_albums=250

random.shuffle(albums)
for i, album_path in enumerate(albums):
    parts = album_path.split(os.path.sep)
    album = parts[-1]
    artist = parts[-2]
    d=os.path.join(dst, f'{i+1:03d}-{artist}-{album}')
    print(f'{album_path} -> {d}')
    copy_tree(album_path, d)
    if ctrl_c_exit or i >= num_albums-1:
        break
