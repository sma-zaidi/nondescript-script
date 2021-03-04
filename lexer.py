import ply.lex as lex

reserved = [
    'TYPE', # double, int, char, string, bool, list
    'DO',
    'WHILE',
    'LIST',
    'STANDARD_OUT' # print
]

data = [ # literals
    'DOUBLE',
    'INT',
    'CHAR',
    'STRING',
    'BOOL'
]

numerical_operators = [
    'INCREMENT',
    'DECREMENT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EXPONENT',
    'MODULO'
]

logical_operators = [
    'EQUALS',
    'NOTEQUALS',
    'LESSTHANEQUALS',
    'GREATERTHANEQUALS',
    'LESSTHAN',
    'GREATERTHAN',
    'NOT',
    'AND',
    'OR'
]

syntax = [
    'IDENTIFIER',
    'ASSIGNMENT', # =
    'BRACE_OPEN',
    'BRACE_CLOSE',
    'PARENTHESIS_OPEN',
    'PARENTHESIS_CLOSE',
    'BRACKET_OPEN',
    'BRACKET_CLOSE',
    'END_OF_STATEMENT'
]

tokens = []
for token in reserved: tokens.append(token)
for token in data: tokens.append(token)
for token in numerical_operators: tokens.append(token)
for token in logical_operators: tokens.append(token)
for token in syntax: tokens.append(token)

## reserved ##
def t_TYPE(token):
    r'double | int | char | string | bool'
    return token

def t_LIST(token):
    r'list'
    return token

def t_DO(token):
    r'do'
    return token

def t_WHILE(token):
    r'while'
    return token

def t_STANDARD_OUT(token):
    r'print'
    return token

## literals ##
def t_DOUBLE(token):
    r'[0-9]+\.[0-9]+'
    token.value = float(token.value)
    return token

def t_INT(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

def t_CHAR(token):
    r'\'.\''
    token.value = token.value.strip("'")
    return token

def t_STRING(token):
    r'"[^\"]*"'
    token.value = token.value.strip('"')
    return token

def t_BOOL(token):
    r'true | false'
    if token.value == 'true': token.value = True
    else: token.value = False
    return token

## numerical operators ##
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EXPONENT = r'\^'
t_MODULO = r'\%'

## logical operators ##
t_EQUALS = r'\=\='
t_NOTEQUALS = r'\!\='
t_LESSTHANEQUALS = r'\<\='
t_GREATERTHANEQUALS = r'\>\='
t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'

def t_NOT(token):
    r'NOT'
    return token

def t_AND(token):
    r'AND'
    return token

def t_OR(token):
    r'OR'
    return token

## syntax ##
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_ASSIGNMENT = r'\='
t_BRACE_OPEN = r'\{'
t_BRACE_CLOSE = r'\}'
t_PARENTHESIS_OPEN = r'\('
t_PARENTHESIS_CLOSE = r'\)'
t_BRACKET_OPEN = r'\['
t_BRACKET_CLOSE = r'\]'
t_END_OF_STATEMENT = r'\;'

t_ignore = ' \t\n,' # ignore spaces, tabs and newlines

def t_error(token):
    print('Unrecognized token "%s" on line %d.' % (token.value, token.lexer.lineno))
    token.lexer.skip(1)

lexer = lex.lex()

######################################
######################################

if __name__ == '__main__': # debugging
    while True:
        lexer.input(input('>> '))
        while True:
            token = lexer.token()
            if token:
                print(token)
            else: break



