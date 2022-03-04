from ply import lex
import ply.yacc as yacc

tokens = (
    'PLUS',
    'MINUS',
    'TIMES',
    'DIV',
    'LPAREN',
    'RPAREN',
    'NUMBER',
    'EQUALS',
    'INT',
    'FLOAT',
    'NAME',
)

#token semantics
t_ignore = ' \t'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIV     = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS = r'\='

#defining the elements of a NUMBER
def t_NUMBER( t ) :
    r'[0-9]+'
    t.value = int( t.value )
    return t

#defining the element of a FLOAT
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

#defingin the element of an INT
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

#defining the elements of a NAME
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

#displays a new line
def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

#token error handling
def t_error( t ):
  print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )

#runs lex
lexer = lex.lex()

#Operator precedence grammer
precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIV' ),
    ( 'nonassoc', 'UMINUS' )
)

# assigns an expression to a variable name
def p_var_assign(p): 
    '''
    var_assign : NAME EQUALS expr
    '''
    p[0] = ('=', p[1], p[3])

#command adds two expressions
def p_add( p ) :
    'expr : expr PLUS expr'
    p[0] = p[1] + p[3]

#command minus two expressions
def p_sub( p ) :
    'expr : expr MINUS expr'
    p[0] = p[1] - p[3]

#command negates the second element and stores the result in the first element
def p_expr2uminus( p ) :
    'expr : MINUS expr %prec UMINUS'
    p[0] = - p[2]

#command multiplies or divides two expressions
def p_mult_div( p ) :
    '''expr : expr TIMES expr
            | expr DIV expr'''

    if p[2] == '*' :
        p[0] = p[1] * p[3]
    else :
        if p[3] == 0 :
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        p[0] = p[1] / p[3]

#command assigns a NUMBER to an expression
def p_expr2NUM( p ) :
    'expr : NUMBER'
    p[0] = p[1]

def p_expr_int_float(p):
    '''
    expr : INT
         | FLOAT
    '''
    p[0] = p[1]


#creates a variable name
def p_expr_var(p):
    '''
    expr : NAME
    '''
    p[0] = ('var', p[1])

#command assigns Parenthesis
def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

#displays an error message for an input
def p_error( p ):
    print("Syntax error in input!")

#assigns None to an empty element
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

#runs yacc
parser = yacc.yacc()

def codeAccept(code):
    print(code)
    res = parser.parse(code) # the input
    compiledTo = {
        "compiled": res
    }

    return compiledTo