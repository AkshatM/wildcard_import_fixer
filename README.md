# About

A short and sweet command line utility to find all names that have been imported with a universal (AKA wildcard) import and replace them with less dangerous import structures.

Turn this:

```
from numpy import *
    
x = array([1])
```

into this:

```
import numpy
x = numpy.array([1])
```

# Motivation

- [This StackOverflow question](http://stackoverflow.com/questions/39403430/is-there-a-tool-to-check-what-names-i-have-used-from-a-wildly-imported-module), indicating there are people in this world eager to atone for the sins of their imports.
- Universal imports can make future maintenance nightmarish and impossible, as [lots of people have complained in the past](https://pythonconquerstheuniverse.wordpress.com/2011/03/28/why-import-star-is-a-bad-idea/). They are not recommended by [PEP8](http://legacy.python.org/dev/peps/pep-0008/#imports).

Hopefully, this tool can help mitigate some of the pain involved in identifying what's what and cleaning up code a little.

# Usage

```
age: universal-fixer.py [-h] [--replace] file_path

Find all function names from universal imports and fix them!

positional arguments:
  file_path   Python file to find and replace universal imports in

optional arguments:
  -h, --help  show this help message and exit
  --replace   Indicate you want to replace found matches to conform to PEP8 standard for wildcard import. 
              Omitted, universal-fixer only searches and displays found matches, but does not alter the actual file.
```
