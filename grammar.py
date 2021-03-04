import ply.yacc as yacc
from lexer import *
from environment import *

precedence = (
    ('nonassoc', 'STANDARD_OUT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'EXPONENT')
)

def p_program(p):
    '''
    program : statement
            | program statement
            | empty
    '''
    if len(p) == 2: run(p[1])
    else: run(p[2])

def p_statements(p): # parse multiple expressions for the multiple object stdout thing
    '''
    statements : statement
               | statement statements
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else: p[0] = [p[1]] + p[2]

def p_statement(p):
    '''
    statement : instruction END_OF_STATEMENT
    '''
    p[0] = p[1]

def p_instruction(p):
    '''
    instruction  : stdout
                 | declaration
                 | assignment
                 | increment
                 | list
                 | dowhile
    '''
    p[0] = p[1]

def p_dowhile(p):
    '''
    dowhile : DO statements WHILE expression
    '''
    p[0] = ('dowhile', p[2], p[4])

def p_stdout(p):
    '''
    stdout : STANDARD_OUT expressions
    '''
    p[0] = ('print', p[2])

def p_declaration(p):
    '''
    declaration : TYPE IDENTIFIER
                | LIST IDENTIFIER
    '''
    p[0] = ('declare', p[2], p[1])

def p_declaration_assignment(p):
    '''
    declaration : TYPE IDENTIFIER ASSIGNMENT expression
                | LIST IDENTIFIER ASSIGNMENT expressions
    '''
    p[0] = ('declare-assign', p[2], p[4], p[1])

def p_assignment(p):
    '''
    assignment : IDENTIFIER ASSIGNMENT expression
    '''
    p[0] = ('assign', p[1], p[3])

def p_increment(p): # handles increment and decrement
    '''
    increment : IDENTIFIER INCREMENT
              | IDENTIFIER DECREMENT
    '''
    p[0] = (p[2], p[1])

def p_list_expression(p):
    '''
    list : expression
    '''
    p[0] = p[1]

def p_list_change(p): # list push/pop
    '''
    expression : IDENTIFIER INCREMENT expressions
               | IDENTIFIER DECREMENT INT
    '''
    p[0] = ('list' + p[2], p[1], p[3])

def p_list_slice(p):
    '''
    expression : IDENTIFIER BRACKET_OPEN INT INT BRACKET_CLOSE
    '''
    p[0] = ('list_slice', p[1], p[3], p[4])

def p_expressions(p): # parse multiple expressions for the multiple object stdout thing
    '''
    expressions : expression
                | expression expressions
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else: p[0] = [p[1]] + p[2]

def p_expression_negate(p):
    '''
    expression : MINUS INT
    '''
    p[0] = ('negate', p[2])

def p_expression_parenthesis(p):
    '''
    expression : PARENTHESIS_OPEN expression PARENTHESIS_CLOSE
    '''
    p[0] = p[2]

def p_expression_binary(p):
    '''
    expression : expression EXPONENT expression
               | expression MODULO expression
               | expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression EQUALS expression
               | expression NOTEQUALS expression
               | expression LESSTHANEQUALS expression
               | expression GREATERTHANEQUALS expression
               | expression LESSTHAN expression
               | expression GREATERTHAN expression
               | expression AND expression
               | expression OR expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_not(p):
    '''
    expression : NOT expression
    '''
    p[0] = (p[1], p[2])

def p_expression_identifier(p):
    '''
    expression : IDENTIFIER
    '''
    p[0] = ('access', p[1])

def p_expression_list_index(p):
    '''
    expression : IDENTIFIER BRACKET_OPEN INT BRACKET_CLOSE 
    '''
    p[0] = ('list_index', p[1], p[3])

def p_expression(p):
    '''
    expression : INT
               | DOUBLE
               | CHAR
               | STRING
               | BOOL
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty : 
    '''
    p[0] = None

env = Environment()

def onError(error):
    print(error)
    raise SystemExit

def run(p):
    if type(p) == tuple:
        if p[0] == '^':
            return run(p[1]) ** run(p[2])
        elif p[0] == '%':
            return run(p[1]) % run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '==':
            return run(p[1]) == run(p[2])
        elif p[0] == '!=':
            return run(p[1]) != run(p[2])
        elif p[0] == '<=':
            return run(p[1]) <= run(p[2])
        elif p[0] == '>=':
            return run(p[1]) >= run(p[2])
        elif p[0] == '<':
            return run(p[1]) < run(p[2])
        elif p[0] == '>':
            return run(p[1]) > run(p[2])
        elif p[0] == 'AND':
            return run(p[1]) and run(p[2])
        elif p[0] == 'OR':
            return run(p[1]) or run(p[2])
        elif p[0] == 'NOT':
            return not run(p[1])

        elif p[0] == 'negate':
            return -1 * p[1]

        elif p[0] == 'declare':
            try: env.declare(p[2], p[1])
            except: onError("RedeclarationError")

        elif p[0] == 'declare-assign':
            try: env.declare(p[3], p[1], run(p[2]))
            except TypeError: onError("TypeError")
            except: onError("RedeclarationError")

        elif p[0] == 'assign':
            try: env.assign(p[1], run(p[2]))
            except TypeError: onError("TypeError")
            except NameError: onError("NameError")

        elif p[0] == 'access':
            try: return env.access(p[1])
            except NameError: raise

        elif p[0] == 'list++': # push
            try:
                target = env.access(p[1])
                target.extend(p[2])
            except NameError: onError("NameError")

        elif p[0] == 'list--': # pop
            try:
                target = env.access(p[1])
                if p[2] < len(target):
                    return target.pop(p[2])
                else:
                    raise IndexError
            except NameError: onError("NameError")

        elif p[0] == 'list_index':
            try:
                target = env.access(p[1])
                if p[2] < len(target):
                    return target[p[2]]
                else:
                    raise IndexError
            except: raise

        elif p[0] == 'list_slice':
            try:
                target = env.access(p[1])
                if p[2] >= 0 and p[3] <= len(target) and p[2] <= p[3]:
                    return target[p[2]:p[3]]
                else:
                    raise IndexError
            except: raise NameError

        elif p[0] == '++':
            try: env.assign(p[1], env.access(p[1]) + 1)
            except TypeError: onError("TypeError")
            except TypeError: onError("NameError")

        elif p[0] == '--':
            try: env.assign(p[1], env.access(p[1]) - 1)
            except TypeError: onError("TypeError")
            except TypeError: onError("NameError")

        elif p[0] == 'dowhile':
            env.push()
            run(p[1])
            env.pop()
            while run(p[2]):
                env.push()
                for expression in p[1]:
                    run(expression)
                env.pop()
            
        elif p[0] == 'print':
            try:
                for expression in p[1]:
                    result = run(expression)
                    if type(result) == bool:
                        if result == True: result = 'true'
                        else: result = 'false'
                    print(result, end = ' ')
                print()
            except IndexError: onError("IndexError")
            except NameError: onError("NameError")
            except TypeError: onError("TypeError")
            except: pass

    else:
        return p

parser = yacc.yacc()

if __name__ == '__main__':
    while True:
        line = input('>> ')
        parser.parse(line)

