#!/usr/bin/env python

import argparse
import sys

from linkTests import run_link_tests

def __run_all():
    run_link_tests()

def __link_tests(article_name):
    run_link_tests(article_name)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        __run_all()
    elif len(sys.argv) == 2:
        __link_tests(sys.argv[1])
