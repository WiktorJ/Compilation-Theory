#!/usr/bin/python

import sys
import ply.lex as lex

def find_tok_column( token):
      last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
      if last_cr < 0:
        last_cr = 0
      return token.lexpos - last_cr


def build(self):
      self.lexer = lex.lex(object=self)

def input( text):
      self.lexer.input(text)

def token(self):
      return self.lexer.token()



literals = "{}()<>=;:,+-*/%&|^"


reserved = {
   'break'   : 'BREAK',
   'continue': 'CONTINUE',
   'if'      : 'IF',
   'else'    : 'ELSE',
   'print'   : 'PRINT',
   'repeat'  : 'REPEAT',
   'return'  : 'RETURN',
   'while'   : 'WHILE',
   'until'   : 'UNTIL',
  }


tokens = [ "AND", "EQ", "FLOAT", "GE", "ID", "INTEGER", "LE", "NEQ", "OR",
             "SHL", "SHR", "STRING", "TYPE",  ] + list(reserved.values())


t_ignore = ' \t\f'

def t_newline(t):
      r'\n+'
      t.lexer.lineno += len(t.value)

def t_newline2(t):
      r'(\r\n)+'
      t.lexer.lineno += len(t.value) / 2


def t_error(t):
      print("Illegal character '{0}' ({1}) in line {2}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
      t.lexer.skip(1)


def t_LINE_COMMENT(t):
      r'\#.*'
      pass

def t_BLOCK_COMMENT(t):
      r'/\*(.|\n)*?\*/'
      t.lexer.lineno += t.value.count('\n')


def t_FLOAT(t):
      r"\d+(\.\d*)|\.\d+"
      return t

def t_INTEGER(t):
      r"\d+"
      return t

def t_STRING(t):
      r'\"([^\\\n]|(\\.))*?\"'
      return t


t_EQ = r"=="
t_NEQ = r"!="
t_LE = r"<="
t_GE = r">="
t_OR = r"\|\|"
t_AND = r"&&"
t_SHL = r"<<"
t_SHR = r">>"


def t_TYPE(t):
      r"\b(int|float|string)\b"
      return t

def t_ID(t):
      r"[a-zA-Z_]\w*"
      t.type = reserved.get(t.value, 'ID')
      return t


lexer = lex.lex()
fh = None
try:
    fh = open(sys.argv[1] if len(sys.argv) > 1 else "plik.ini", "r");
    lexer.input( fh.read() )
    for token in lexer:
        print("line %d: %s(%s)" %(token.lineno, token.type, token.value))
except:
    print("open error\n")
