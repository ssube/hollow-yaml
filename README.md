# Hollow YAML

Removes values, leaves, and selected branches from YAML documents. Perfect for redacting secrets and documenting
the structure of documents.

## Build

```shell
pip3 install -r requirements.txt
```

## Run

Provide an input file:

```shell
$ ./hollow.py -f examples/simple.yml

foo:
  hello: ''
```

Get help:

```shell
$ ./hollow.py -h
usage: hollow.py [-h] ...

remove values from yaml document
...
```