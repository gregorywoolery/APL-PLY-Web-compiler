# -*- coding: utf-8 -*-
# Portions of this code were adapted from 
# https://www.dabeaz.com/ply/ply.html#ply_nn5
# David M. Beazley

# Creators:
# Gregory Woolery
# Matthew Ruddock
# McKiba Williams


import datetime
from msilib.schema import Error
from PyQt5 import QtCore, QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
import os
import ply.lex as lex
import ply.yacc as yacc
import PyInstaller.__main__
from datetime import datetime

# Create the environment upon which we will store and retreive variables from.
env = {}
# Create interator to store current line being executed
currentLine = 0

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
    'PRINT',
    'COMMA'
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
t_COMMA = r'\,'



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

def t_PRINT(t):
    r'PRINT'
    t.type = 'PRINT'
    return t

# A NAME is a variable name. A variable can be 1 or more characters in length.
# The first character must be in the ranges a-z A-Z or be an underscore.
# Any character following the first character can be a-z A-Z 0-9 or an underscore.
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

# Skip the current token and output 'Illegal characters' using the special Ply t_error function.
def t_error(t):
    setError("Error line: %d: LEXER: Illegal characters '%s'" % (t.lexer.lineno, t.value[0]))
    # STOP LEXER
    # ====================
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


#PARSER
# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.

precedence = (
    ('right','COMMA'),
    ('nonassoc', 'PRINT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'EXPONENTIATION', 'MULTIPLY'),
)

# Define our grammar. We allow var_assign's and empty's.
def p_start(p):
    '''
    start : statement
          | var_assign
          | empty
    '''
    run(p[1])


def p_statement_print(p):
    '''
    statement : PRINT NORMSTRING 
              | PRINT expression 
              | PRINT expression COMMA expression
              | PRINT NORMSTRING COMMA expression
    '''
    if len(p) == 5: 
        p[0] = ('PRINT', p[2], p[4])
    else:
        p[0] = ('PRINT', p[2])


def p_statement_print_error(p):
    '''
    statement : PRINT error
    '''
    setError("Syntax error in print statement. Bad expression")

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
               | NAME EQUALS NORMSTRING
    '''
    # Build our tree
    p[0] = ('=', p[1], p[3])

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

def p_expression_parenthesis_error(p):
    setError("Parenthesis error found! %s" % p)

	

# Output to the user that there is an error in the input as it doesn't conform to our grammar.
# p_error is another special Ply function.
def p_error(p):
    if p is not None:
        if p.type == 'NORMSTRING':
            setError("Syntax error on line %s with print statement" % (currentLine))
        else:
            setError("Syntax error on line %s." % (currentLine))
    else:
        setError("Line %s - Unexpected end of input" % (currentLine))

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# Build the parser
parser = yacc.yacc()

# The run function is our recursive function that 'walks' 
# the tree generated by our parser.
def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2]) #eg. 5 + 5
        elif p[0] == '-':
            return run(p[1]) - run(p[2]) #eg. 5 - 5
        elif p[0] == '*':
            return run(p[1]) * run(p[2]) #eg. 5 * 5
        elif p[0] == '/':
            return run(p[1]) / run(p[2]) #eg. 5 / 5
        elif p[0] == '^':
            return run(p[1]) ** run(p[2]) #eg 5 ^ 5
        elif p[0] == '=':
            env[p[1]] = run(p[2])         #eg. a = 5

            if(env[p[1]] is None):
                setError('Line %s - Variable referenced before being initialized' % (currentLine));
            return ''
        
        #Print Syntax Handler
        elif p[0] == 'PRINT':
            if len(p) == 3: 
                value1 = run(p[1])
                value2 = run(p[2])
                setOutput(value1, value2) #Create python file and add print statement -> create exe & machine code file
            else:
                value1 = run(p[1])
                setOutput(value1)   #Create python file and add print statement -> create exe & machine code file

        #This handler gets the variable from the current running interpreting
        elif p[0] == 'var':
            if p[1] not in env:
                setError('Line %s - Undeclared variable found!' % (currentLine))
            else:
                return env[p[1]]
    else:
        return p


#Sets error flag, prints error message on console 
#and raises error to the interpreting to stop interpreting
def setError(error):
    setConsoleMessage('Error: ' + error)
    raise Error


#Writes output to temporary python file to be converted to exe
#Writes to the console the output of the interpreter
def setOutput(message1, message2 = ''):
    outString1 = str(message1)
    outString2 = str(message2)

    if outString1.startswith('"') and outString1.endswith('"') :
        outString1 = outString1.strip('"')
    if outString2.startswith('"') and outString2.endswith('"') :
        outString2 = outString2.strip('"')
    newString = outString1 + outString2

    writeToFile(newString)
    setConsoleMessage(newString)


#Writes to the GUI Console any message with the date and time recorded
def setConsoleMessage(message):
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    display_string = dt_string + " - " + message

    error_text_box.append(display_string);


#Entry point where code to be interpretted is sent into
#Function gets code from GUI and parses through each line
def codeAccept():
    try:
        setConsoleMessage("interpreting... please wait")
        
        #Remove file if exists
        if os.path.exists("snake.py"):
            os.remove("snake.py")

        code = code_text_box.toPlainText();

        # Place code in separate lines
        arr = code.splitlines()

        # Parse through code line by line
        global currentLine
        for line in arr:
            currentLine += 1
            parser.parse(line)

        setConsoleMessage("Interpreting Finished.");
        
        #Reinitialize interpreter environment to be able to write new program
        reinitializeENV();

        setConsoleMessage("Creating .exe file.");

        # Break point in .exe to pause
        snake = open("snake.py", 'a')
        line = 'input("Press Enter to close")'
        snake.write(line)
        snake.close()

        #Creates an exe file based on interpreter output that is to be ran
        PyInstaller.__main__.run([
        '--onefile',
        'snake.py',
        ])

        #Removes temporary .py file from project
        if os.path.exists("snake.py"):
            os.remove("snake.py")

        setConsoleMessage(".exe file is now ready ! Go to dist/snake.exe");
    except :
        reinitializeENV()
        pass


#Writes to temporary .py file python output from interpreter
def writeToFile(line):
    snake = open("snake.py", 'a')
    line = 'print("%s")\n' % line
    snake.write(line)
    snake.close()


#Reinitializes interpreter environment to accept new variables and current lines
def reinitializeENV():
    global env
    global currentLine
    env = {}
    currentLine = 0



# GUI Configuration
MainWindow.setObjectName("MainWindow")
MainWindow.resize(1169, 942)
MainWindow.setStyleSheet("background-color: rgb(0, 0, 57);")
centralwidget = QtWidgets.QWidget(MainWindow)
centralwidget.setObjectName("centralwidget")
run_button = QtWidgets.QPushButton(centralwidget, clicked = lambda: codeAccept())
run_button.setGeometry(QtCore.QRect(1000, 40, 81, 41))
run_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(56, 168, 0);\n"
"font-weight: bold;\n"
"border-radius: 10px;\n"
"")
run_button.setObjectName("run_button")
clear_button = QtWidgets.QPushButton(centralwidget, clicked = lambda: code_text_box.clear())
clear_button.setGeometry(QtCore.QRect(850, 40, 81, 41))
clear_button.setStyleSheet("background-color: rgb(188, 0, 0);\n"
"border-radius: 10px;\n"
"font-weight: bold;\n"
"color: rgb(255, 255, 255);")
clear_button.setObjectName("clear_button")
code_text_box = QtWidgets.QTextEdit(centralwidget)
code_text_box.setGeometry(QtCore.QRect(30, 90, 1101, 601))
code_text_box.setStyleSheet("border-radius: 5px;\n"
"font: 75 11pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(0, 0, 57);\n"
"border: 1px solid #fff;\n"
"color: rgb(188, 188, 188);\n"
"padding: 5px;\n"
"")
code_text_box.setObjectName("code_text_box")
error_text_box = QtWidgets.QTextEdit(centralwidget)
error_text_box.setEnabled(True)
error_text_box.setGeometry(QtCore.QRect(20, 780, 1131, 121))
error_text_box.setStyleSheet("border-radius: 5px;\n"
"padding: 5px;\n"
"padding-top: 17px;\n"
"color: rgb(188, 188, 188);\n"
"font: 9pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(13, 9, 54);\n"
"border: 1px solid #fff;")
error_text_box.setReadOnly(True)
error_text_box.setObjectName("error_text_box")
terminal_label = QtWidgets.QLabel(centralwidget)
terminal_label.setGeometry(QtCore.QRect(20, 729, 341, 51))
terminal_label.setStyleSheet("color: rgb(255, 0, 127);\n"
"background-color: rgb(14, 9, 82);\n"
"text-decoration: underline;\n"
"padding-left: 10px;\n"
"border-bottom: 1px solid #fff;\n"
"font-size: 16px;")
terminal_label.setObjectName("terminal_label")
terminal_label_2 = QtWidgets.QLabel(centralwidget)
terminal_label_2.setGeometry(QtCore.QRect(360, 729, 791, 51))
terminal_label_2.setStyleSheet("color: rgb(255, 0, 127);\n"
"background-color: rgb(14, 9, 82);\n"
"text-decoration: underline;\n"
"padding-left: 10px;\n"
"border-bottom: 1px solid #fff;")
terminal_label_2.setText("")
terminal_label_2.setObjectName("terminal_label_2")
clear_button_2 = QtWidgets.QPushButton(centralwidget, clicked= lambda: error_text_box.clear())
clear_button_2.setGeometry(QtCore.QRect(1070, 740, 61, 31))
clear_button_2.setStyleSheet("background-color: rgb(188, 0, 0);\n"
"border-radius: 10px;\n"
"font-weight: bold;\n"
"color: rgb(255, 255, 255);\n"
"font-size: 11px;\n"
"")
clear_button_2.setObjectName("clear_button_2")
file_label_3 = QtWidgets.QLabel(centralwidget)
file_label_3.setGeometry(QtCore.QRect(40, 30, 171, 61))
file_label_3.setStyleSheet("color: rgb(255, 0, 127);\n"
"background-color: rgb(14, 9, 82);\n"
"padding-left: 10px;\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"border-bottom: 1px solid #fff;\n"
"font-size: 16px;\n"
"")
file_label_3.setObjectName("file_label_3")
file_label_4 = QtWidgets.QLabel(centralwidget)
file_label_4.setGeometry(QtCore.QRect(810, 30, 311, 61))
file_label_4.setStyleSheet("color: rgb(255, 0, 127);\n"
"background-color: rgb(14, 9, 82);\n"
"padding-left: 10px;\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"border-bottom: 1px solid #fff;")

file_label_4.setText("")
file_label_4.setObjectName("file_label_4")
code_text_box.raise_()
error_text_box.raise_()
terminal_label.raise_()
terminal_label_2.raise_()
clear_button_2.raise_()
file_label_3.raise_()
file_label_4.raise_()
run_button.raise_()
clear_button.raise_()
MainWindow.setCentralWidget(centralwidget)
statusbar = QtWidgets.QStatusBar(MainWindow)
statusbar.setObjectName("statusbar")
MainWindow.setStatusBar(statusbar)

QtCore.QMetaObject.connectSlotsByName(MainWindow)

_translate = QtCore.QCoreApplication.translate

MainWindow.setWindowTitle(_translate("MainWindow", "SnakePY"))
run_button.setText(_translate("MainWindow", "RUN"))
clear_button.setText(_translate("MainWindow", "CLEAR"))
code_text_box.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:72; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

error_text_box.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

terminal_label.setText(_translate("MainWindow", "Terminal - bash"))
clear_button_2.setText(_translate("MainWindow", "EMPTY"))
file_label_3.setText(_translate("MainWindow", "SnakePy.py"))
# GUI Configuration end


#Initialize gui
while 1:
    try:
        MainWindow.show()
        sys.exit(app.exec_())
    except EOFError:
        break
