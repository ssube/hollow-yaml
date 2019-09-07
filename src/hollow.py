#! /usr/bin/env python3

import argparse
import sys
from enum import Enum
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq
from ruamel.yaml.tokens import CommentToken


class Next(Enum):
    RECURSE = 1
    REDACT = 2
    RETAIN = 3
    RELIST = 4


parser = argparse.ArgumentParser(
    description="remove values from yaml document")
parser.add_argument("-f", "--file", help="input file")


def empty_value(data):
    dt = type(data)

    if dt is bool:
        return False
    elif dt is int:
        return 0
    elif dt is str:
        return ''
    elif dt is CommentedSeq:
        return []

# detect leaves


def is_leaf(data, cmt):
    if cmt != "":
        #print('checking leaf with comment', cmt)
        if "@retain" in cmt:
            return Next.RETAIN
        elif "@redact" in cmt:
            return Next.REDACT

    dt = type(data)
    #print("checking leaf type: %s (%s)" % (data, dt))

    if dt is bool:
        return Next.REDACT
    elif dt is int:
        return Next.REDACT
    elif dt is str:
        return Next.REDACT
    elif dt is CommentedSeq:
        return Next.RELIST
    elif dt is list:
        return Next.RELIST
    else:
        return Next.RECURSE

# load a yaml document from file


def load_doc(path, yaml):
    try:
        with open(path, 'r') as doc:
            data = yaml.load(doc)
            return data

    except Exception as err:
        print("Error loading YAML: %s" % err)
        sys.exit(1)


def build_comment(items):
    cmt = ""
    for i in items:
        it = type(i)
        if it == list:
            cmt += build_comment(i)
        elif it == CommentToken:
            cmt += i.value

    return cmt.strip()


def strip_list(data):
    return []

# remove values, leaves, and marked branches


def strip_branch(data):
    #print('stripping branch', type(data), data)
    for key in data:
        val = data[key]
        cmt = build_comment(data.ca.items[key]) if key in data.ca.items else ""

        #print("checking data key: %s = %s (%s)" % (key, val, cmt))
        next = is_leaf(val, cmt)

        if next == Next.RECURSE:
            strip_branch(val)
        elif next == Next.RELIST:
            data[key] = strip_list(val)
        elif next == Next.REDACT:
            data[key] = empty_value(val)


def main(args):
    args = parser.parse_args(args)

    yaml = YAML()
    data = load_doc(args.file, yaml)
    strip_branch(data)
    yaml.dump(data, sys.stdout)


if __name__ == "__main__":
    main(sys.argv[1:])
