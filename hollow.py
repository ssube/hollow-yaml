#! /usr/bin/env python3

import argparse, sys
from ruamel.yaml import YAML

parser = argparse.ArgumentParser(description="remove values from yaml document")
parser.add_argument("-f", "--file", help="input file")

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
  stripped = dict()

  for key in data:
    val = data[key]
    tval = type(val)

    if tval is bool:
      stripped[key] = False
    elif tval is int:
      stripped[key] = 0
    elif tval is str:
      stripped[key] = ""
    else:
      stripped[key] = strip_branch(val)
  
  return stripped

def main(args):
  args = parser.parse_args(args)

  yaml = YAML()
  data = load_doc(args.file, yaml)
  data = strip_branch(data)
  yaml.dump(data, sys.stdout)

if __name__ == "__main__":
  main(sys.argv[1:])