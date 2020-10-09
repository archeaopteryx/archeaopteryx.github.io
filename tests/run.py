#!/usr/bin/env python

import argparse
import sys

from linkTests import run_link_tests

def __run_all():
    run_link_tests()

def __link_tests(args):
    run_link_tests(args.article_file)

def __cli_parse():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    link_text = "Tests header links, quick nav links, and archive links. Can be run for all files, or a single article."
    parser_links = subparser.add_parser("link-test")
    parser_links.add_argument('article_file', nargs='?', default=None)
    parser_links.set_defaults(func=__link_tests)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        __run_all()
    else:
        __cli_parse()
