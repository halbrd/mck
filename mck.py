#!/usr/bin/env python

import argparse
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(levelname)8s: %(message)s',
)

def check(file, formats):
    pass

def spek(file):
    pass

def convert(file, output_format):
    pass


parser = argparse.ArgumentParser()

parser.add_argument('action',
    choices=['check', 'spek', 'convert'],
    help='specify task to perform')
parser.add_argument('path',
    default='.',
    help='specify path to find music in')
parser.add_argument('--select-formats',
    nargs='*',
    default=['m4a', 'flac', 'mp3'],
    metavar='formats',
    help='filter inputs by file format')
parser.add_argument('--output-format',
    help='specify output file format for the `convert` action')

args = parser.parse_args()

files = Path(args.path).glob('**/*')

for file in files:

    if args.action == 'check':
        check(file, args.formats)

    elif args.action == 'spek':
        spek(file)

    elif args.action == 'convert':
        convert(file, args.output_format)
