import sys
from grammar import *

program = '''

'''

if len(sys.argv) >= 2: # define code above, or pass a file as an argument
    with open(sys.argv[1]) as file:
        program = file.read()

parser.parse(program)