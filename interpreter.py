import sys
from grammar import parser

program = '''print "hello world";'''

if len(sys.argv) >= 2: # define code above, or pass a file as an argument
    with open(sys.argv[1]) as file:
        program = file.read()

parser.parse(program)