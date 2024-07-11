#!/usr/bin/python3

import pyperclip
import re

import argparse
import logging
import sys
import random

logging.basicConfig(level=logging.INFO)


def main():
    argparser = argparse.ArgumentParser(description='Remove newlines while optionally keeping double newlines and/or lines ending with punctuation.')
    argparser.add_argument('text', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Input file; or default stdin. Is overruled by option -c.')
    argparser.add_argument('-p', '--punct', action='store_true', help='To keep newlines after sentence-final punctuation mark.')
    argparser.add_argument('-d', '--double', action='store_true', help='To keep double newlines, replacing them by single newlines.')
    argparser.add_argument('-c', '--clipboard', action='store_true', help='To modify clipboard contents; overrides text parameter.')

    args = argparser.parse_args()

    if args.clipboard:
        text = pyperclip.paste()
    else:
        text = args.text.read()

    newline_marker = '<<REINSERT_NEWLINE_HERE>>'
    while newline_marker in text:
        logging.warning('Lol impossible.')
        chars = list(newline_marker)
        random.shuffle(chars)
        newline_marker = ''.join(chars)

    if args.punct:
        text = re.sub(r'([.?!])\n', f'\1{newline_marker}', text)
    if args.double:
        text = re.sub(r'\n\n', newline_marker, text)

    text = re.sub(r'\n', r' ', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n ', '\n', text)

    text = text.replace(newline_marker, '\n')

    if args.clipboard:
        pyperclip.copy(text)
        logging.info("Clipboard contents replaced successfully.")
    else:
        print(text)


if __name__ == '__main__':
    main()
