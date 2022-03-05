from asyncio import constants
import ply.lex as lex
import ply.yacc as yacc
import sys

# Create a list to hold all of the token names
tokens = [

    'NORMSTRING',
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EXPONENTIATION',
    'EQUALS',
    
    'LPAREN',
    'RPAREN',
    'COMMENT',
]

# Use regular expressions to define what each token is
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NORMSTRING =  r'\"([^\\\n]|(\\.))*?\"'
t_EXPONENTIATION = r'\^'



# Ply's special t_ignore variable allows us to define characters the lexer will ignore.
# We're ignoring spaces.
# A string containing ignored characters (spaces and tabs)
t_ignore = '  \t\r'
t_ignore_COMMENT = r'\#.*'

# More complicated tokens, such as tokens that are more than 1 character in length
# are defined using functions.
# A float is 1 or more numbers followed by a dot (.) followed by 1 or more numbers again.
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# An int is 1 or more numbers.
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
    print('line: ', t.lexer.lineno)

# def t_NORMSTRING(t):
#     r'\"\"'
#     t.type = 'NORMSTRING'

#     print("Type: %s" % t)

# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

# Skip the current token and output 'Illegal characters' using the special Ply t_error function.
def t_error(t):
    print("Error line: %d: LEXER: Illegal characters '%s'" % (t.lexer.lineno, t.value[0]))
    # STOP LEXER
    # ====================
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# lex.input("1234\n3434@")

# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.
precedence = (

    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'EXPONENTIATION', 'MULTIPLY')

)

# Define our grammar. We allow var_assign's and empty's.
def p_calc(p):
    '''
    calc : expression 
         | var_assign
         | empty
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
               | NAME EQUALS NORMSTRING
    '''
    # Build our tree
    p[0] = ('=', p[1], p[3])

# def p_string(p):
#     '''
#     string : NORMSTRING
#     '''
#     print('Ps0', p[0])
#     print('Ps1', p[1])
#     print('Ps2', p[2])
#     p[0] = ('string', p[1])

# Expressions are recursive.
def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression EXPONENTIATION expression
    '''
    # Build our tree.
    p[0] = (p[2], p[1], p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

def p_expression_parenthesis(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]
	

# # Output to the user that there is an error in the input as it doesn't conform to our grammar.
# # p_error is another special Ply function.
def p_error(p):
    print("Syntax error found!", p)

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Build the parser
parser = yacc.yacc()

# Create the environment upon which we will store and retreive variables from.
env = {}

# The run function is our recursive function that 'walks' the tree generated by our parser.
def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '^':
            return run(p[1]) ** run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
            return ''
        elif p[0] == 'var':
            if p[1] not in env:
                return 'Undeclared variable found!'
            else:
                return env[p[1]]
    else:
        print('This is P', p)   
        return p

# Create a REPL to provide a way to interface with our calculator.
while True:
    # tok = lexer.token()
    # if not tok:
    #     break
    # print(tok.type, tok.value, tok.lineno, tok.lexpos)
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)

def codeAccept(code):
    # Place code in separate lines
    arr = code.splitlines()
    print(arr)

    for line in arr:
        parser.parse(line)
    
    # parser.parse(code)

    compiledTo = {
        "compiled": 'res'
    }

    return compiledTo