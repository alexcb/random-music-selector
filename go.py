#!/usr/bin/env python3
import os
import random
import signal
import re
import argparse

import shutil

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

def get_ignore_regexes(path):
    ignores = []
    with open(path) as f:
        for l in f.readlines():
            l = l.strip()
            if l.startswith('#'):
                continue
            ignores.append(re.compile(l, flags=re.IGNORECASE))
    return ignores

def apply_ignores(albums, ignores):
    l = []
    for album in albums:
        if any(x.match(album) for x in ignores):
            print(f'ignoring {album}')
            continue
        l.append(album)
    return l

def sort_albums_by_mtime(albums):
    albums.sort(key=os.path.getmtime, reverse=True)

parser = argparse.ArgumentParser(description='random albums.')
parser.add_argument('-n', default=100, type=int)
parser.add_argument('--sort', default='random', choices=['random', 'mtime'])

args = parser.parse_args()

ignore_list_path='random-music-selector-ignore'
print(f'reading ignore list {ignore_list_path}')
ignores = get_ignore_regexes(ignore_list_path)

print(f'reading albums (this can take a while)')
albums = get_albums('/media/tyee/music/')

print(f'applying ignore list')
albums = apply_ignores(albums, ignores)

# currently the network drive is encoding directories containing a : with a ~, which breaks things
print(f'Skipping directories containing ~ (FIXME)')
albums = list([x for x in albums if '~' not in x])

print(f'sorting albums by {args.sort}')
if args.sort == 'mtime':
    sort_albums_by_mtime(albums)
elif args.sort == 'random':
    random.shuffle(albums)
else:
    raise RuntimeError('invalid sort choice')

dst='/media/alex/TUNES'

num_albums = args.n

print(f'randomly copying {num_albums} out of a total of {len(albums)}')
for i, album_path in enumerate(albums):
    parts = album_path.split(os.path.sep)
    album = parts[-1]
    artist = parts[-2]
    d=os.path.join(dst, f'{i+1:03d}-{artist}-{album}')
    print(f'{album_path} -> {d}')
    shutil.copytree(album_path, d)
    if ctrl_c_exit or i >= num_albums-1:
        break
