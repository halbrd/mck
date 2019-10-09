#!/usr/bin/env python

import argparse
from pathlib import Path
import logging
import mutagen
import subprocess

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)8s: %(message)s',
)

def check(file, formats):
    if not file.suffix.lstrip('.') in formats:
        return

    mutafile = mutagen.File(str(file))
    bitrate = int(mutafile.info.bitrate / 1000)

    if not bitrate > 200:
        logging.error(f'bitrate too low ({bitrate}kbps): {file}')

def spek(file):
    logging.info('speking ' + file.name)
    subprocess.run(['spek', file.as_posix()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def convert(file, output_format):
    print('converting file ' + str(file)); return
    pass

def check_album(album, formats):
    # check artist/album
    if len(album.name.split(' -- ')) != 2:
        logging.error(f'could not derive album/artist from "{album.name}"')

    # check for cover art
    if not (album / 'cover.jpg').exists:
        logging.error(f'no cover art found for "{album.name}"')

    # check for unexpected files
    for file in album.iterdir():
        if not (
            file.is_dir() and file.name == 'extras'
            or file.is_file() and file.name == 'cover.jpg'
            or file.is_file() and file.suffix.lstrip('.') in formats
        ):
            logging.error(f'unexpected file/folder "{file.name}" found in "{album.name}"')


parser = argparse.ArgumentParser()

parser.add_argument('action',
    choices=['check', 'spek', 'convert'],
    help='specify task to perform')
parser.add_argument('path',
    nargs='?',
    default='.',
    help='specify path to find music in')
parser.add_argument('--select-formats',
    nargs='*',
    default=['m4a', 'flac', 'mp3'],
    metavar='format',
    help='filter inputs by file format')
parser.add_argument('--output-format',
    help='specify output file format for the `convert` action')

args = parser.parse_args()

files = [file for file in Path(args.path).glob('**/*')
    if file.is_file()
    and not 'extras' in file.parts  # we only care about files that are not in extras
    and not file.name == '.plexignore']  # also ignore .plexignore
files = sorted(files)

if args.action == 'check':
    albums = sorted(set([file.parent for file in files]))
    for album in albums:
        check_album(album, args.select_formats)

for file in files:

    if args.action == 'check':
        check(file, args.select_formats)

    elif args.action == 'spek':
        spek(file)

    elif args.action == 'convert':
        convert(file, args.output_format)
