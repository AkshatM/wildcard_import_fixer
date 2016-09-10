import regex
import sys
import argparse

parser = argparse.ArgumentParser(description='Find all function names from universal imports and fix them!')

parser.add_argument('filename', metavar='file_path', type=argparse.FileType('r+'), 
                    nargs=1, help='Python file to find and replace universal imports in')
parser.add_argument('--replace', action="store_true", help="Indicate you want to search and replace. Omitted, universal-fixer only searches and displays")

args = parser.parse_args()

def replacement_confirmation():
    return True if raw_input("Replace this for all matched lines? (y/n)") == "y" else False

## Collect all of our important flags and variables
filename = args.filename[0]
should_replace = args.replace

## obtain the file content, extract the module names, and import the same

file_contents = filename.read()  # get the entire file as a string
search_string = r"from ([a-zA-Z]+) import *"  # regex to find all wildcard-imported module names
module_names = regex.findall(search_string, file_contents)

map(__import__, module_names)  # import ALL of these modules names at once

## parsing and replacing begin here
for module in module_names:

    if should_replace:
        file_contents = file_contents.replace("from {0} import *".format(module), "import {0}".format(module))

    for function_name in sys.modules[module].__dict__:
        
        # skip dunder names e.g. __all__, __version__, __getitem__, etc. These are always considered special.
        if function_name.startswith("__") and function_name.endswith("__"):
            continue 

        # get all matched names that are not preceded by or immediately followed by an underscore, period (preceded by) 
        # or alphanumeric string. This prevents us from matching parts of larger names or functions that belong to a clear
        # namespace e.g. we don't want to match an existing `numpy.array`.
        search_expression = r"(?<![\w\._]){0}(?![_\w])".format(function_name)

        if regex.search(search_expression, file_contents):
            print("Found expression `{0}` that belongs to module namespace `{1}` in following contexts:".format(function_name, module))
            
            # get everything before (i.e. upto start of string) and after (upto end of string) as named groups `before`, `after`.
            # get the actual matched name as `definition`.
            match_expression = "(?P<before>.+)?(?P<definition>{0})(?P<after>.+)?".format(search_expression)

            # lazily split the file into lines
            file_contents_generator = (x.group(0) for x in regex.finditer(r"[^\n]+", file_contents))

            for line_number, line in enumerate(file_contents_generator):
                match = regex.match(match_expression, line)
                
                if match:
                    
                    limiting_view = (79 - len(match.group('definition')) - len("\tLine{0}".format(line_number + 1))) / 2
 
                    # limit the context so that it doesn't exceed 79 characters 
                    context_before = "...{0}".format(match.group('before')[-limiting_view:]) if match.group('before') else ''
                    context_after = "{0}...".format(match.group('after')[:limiting_view]) if match.group('after') else ''

                    print "\tLine {0}: {1}{2}{3}".format(line_number + 1, context_before, match.group('definition'), context_after)

            if should_replace:

                if replacement_confirmation():
                    # replace (say) `array` with `numpy.array` 
                    replacement_expression = "{0}.{1}".format(module, function_name)
                    file_contents = regex.sub(search_expression, replacement_expression, file_contents)
                else:
                    print "Skipping replacement"

filename.seek(0)  # move to start of file
filename.truncate()  # empty file contents
filename.write(file_contents)
