#! /usr/bin/env python3

import argparse, sys
from enum import Enum
from ruamel.yaml import YAML

class Next(Enum):
  RECURSE = 1
  REDACT = 2
  RETAIN = 3

parser = argparse.ArgumentParser(description="remove values from yaml document")
parser.add_argument("-f", "--file", help="input file")

# detect leaves
# TODO: check comments
def is_leaf(data, cmt):
  dt = type(data)
  #print("checking leaf: %s (%s)" % (data, dt))

  if cmt != "" and "keep" in cmt:
    return Next.RETAIN
  elif dt is bool:
    return Next.REDACT
  elif dt is int:
    return Next.REDACT
  elif dt is str:
    return Next.REDACT
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

# remove values, leaves, and marked branches
def strip_branch(data):
  for key in data:
    #print("checking %s" % key)
    val = data[key]

    if key in data.ca.items:
      cmt = "".join([i.value for i in data.ca.items[key] if i != None])
      #print("comment for %s: %s" % (key, cmt))
    else:
      cmt = ""

    next = is_leaf(val, cmt)

    if next == Next.RECURSE:
      strip_branch(val)
    elif next == Next.REDACT:
      data[key] = None

def main(args):
  args = parser.parse_args(args)

  yaml = YAML()
  data = load_doc(args.file, yaml)
  strip_branch(data)
  yaml.dump(data, sys.stdout)

if __name__ == "__main__":
  main(sys.argv[1:])