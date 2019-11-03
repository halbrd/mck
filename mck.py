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

def check_audio(file):
    mutafile = mutagen.File(str(file))
    bitrate = int(mutafile.info.bitrate / 1000)

    if not bitrate > 200:
        logging.error(f'bitrate too low ({bitrate}kbps): {file}')

def spek_audio(file):
    logging.info('speking ' + file.name)
    subprocess.run(['spek', file.as_posix()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ffmpeg_options_for = {
    'm4a': ['-map', '0:a', '-c:a', 'aac', '-b:a', '257k', '-ar', '44100'],
    # note: the output quality for mp3 is shitty but I'm pretty sure it's just because mp3 is a shitty format
    # still, maybe there are some ffmpeg settings that would improve it
    'mp3': ['-q:a', '0', '-map_metadata', '0', '-id3v2_version', '4'],
    'flac': ['-c:a', 'flac'],
}

def convert_audio(file, output_format):
    logging.info(f'converting to {output_format}: {file.name}')

    dest = file.resolve().parent / file.resolve().parent.name
    if dest.is_file():
        raise FileExistsError(f'can\'t convert "{file.name}" because a file named "{dest.name}" already exists in the folder "{dest.name}"')
    if not dest.is_dir():
        dest.mkdir()

    subprocess.run(
        ['ffmpeg', '-y', '-i', file.as_posix(), '-loglevel', 'warning'] \
        + ffmpeg_options_for[output_format] \
        # converted files go in a copy of the original folder, in the original folder
        # eg.      Coldplay -- X&Y/1-01 Square One.flac
        # goes to  Coldplay -- X&Y/Coldplay -- X&Y/1-01 Square One.m4a
        + [dest / file.with_suffix('.' + output_format).name]
    )

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
            or file.is_file() and file.suffix.lstrip('.').lower() in formats
        ):
            logging.error(f'unexpected file/folder "{file.name}" found in "{album.name}"')


parser = argparse.ArgumentParser()

parser.add_argument('action',
    choices=['check', 'spek', 'convert'],
    help='specify task to perform')
parser.add_argument('paths',
    nargs='*',
    default='.',
    metavar='path',
    help='specify path to find music in')
parser.add_argument('--select-formats',
    nargs='*',
    default=ffmpeg_options_for.keys(),
    metavar='format',
    help='filter inputs by file format')
parser.add_argument('--output-format',
    choices=ffmpeg_options_for.keys(),
    default='m4a',
    help='specify output file format for the `convert` action')

args = parser.parse_args()

# find files to operate on
files = [file for path in args.paths for file in Path(path).glob('**/*')
    if file.is_file()
    and not 'extras' in file.parts  # we only care about files that are not in extras
    and not file.name == '.plexignore']  # also ignore .plexignore
files = sorted(files)

# perform checks that need the context of an album
if args.action == 'check':
    albums = sorted(set([file.parent for file in files]))
    for album in albums:
        check_album(album, args.select_formats)

# perform individual file checks
for file in files:

    # only operate on selected audio files
    if not file.suffix.lstrip('.').lower() in args.select_formats:
        continue

    if args.action == 'check':
        check_audio(file)

    elif args.action == 'spek':
        spek_audio(file)

    elif args.action == 'convert':
        convert_audio(file, args.output_format)
