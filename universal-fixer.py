import regex
import sys
import argparse

parser = argparse.ArgumentParser(description='Find all function names from universal imports and fix them!')

parser.add_argument('filename', metavar='file_path', type=argparse.FileType('r+'), 
                    nargs=1, help='Python file to find and replace universal imports in')
parser.add_argument('--replace', action="store_true", help="Indicate you want to search and replace. Omitted, universal-fixer only searches and displays")

args = parser.parse_args()

filename = args.filename[0]
should_replace = args.replace

file_contents = filename.read()  # get the entire file as a string
search_string = r"from ([a-zA-Z]+) import *"  # regex to find all wildcard-imported module names
module_names = regex.findall(search_string, file_contents)

map(__import__, module_names)  # import ALL of these modules names at once

for module in module_names:

    if should_replace:
        file_contents = file_contents.replace("from {0} import *".format(module), "import {0}".format(module))

    for function_name in sys.modules[module].__dict__:
        
        # skip dunder names e.g. __all__, __version__, etc. These are always considered special.
        if function_name.startswith("__") and function_name.endswith("__"):
            continue 

        # get all function names without a preceding dot, as that indicates existing namespace
        search_expression = r"(?<![\._]){0}(?!_)".format(function_name)

        if regex.search(search_expression, file_contents):
            print("Found expression {0} that belongs to module namespace {1}".format(function_name, module))
 
        if should_replace:
            # replace (say) `array` with `numpy.array` 
            replacement_expression = "{0}.{1}".format(module, function_name)

            file_contents = regex.sub(search_expression, replacement_expression, file_contents) 

filename.seek(0)  # move to start of file
filename.truncate()  # empty file contents
filename.write(file_contents)
