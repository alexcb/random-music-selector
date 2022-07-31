#!/usr/bin/env python3
import os
import random

from distutils.dir_util import copy_tree

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

random.shuffle(albums)
for album_path in albums:
    parts = album_path.split(os.path.sep)
    album = parts[-1]
    artist = parts[-2]
    d=os.path.join(dst, artist, album)
    print(f'{album_path} -> {d}')
    copy_tree(album_path, d)
