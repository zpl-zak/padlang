""" PadLang (c) Dominik Madarasz <zaklaus@madaraszd.net> """

###############################################################################
#                                                                             #
#  TOKEN TYPES                                                                #
#                                                                             #
###############################################################################

# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER = 'INTEGER'
REAL = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
INTEGER_MOD = 'INTEGER_MOD'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
ASSIGN = 'ASSIGN'
BEGIN = 'BEGIN'
END = 'END'
SEMI = 'SEMI'
DOT = 'DOT'
PROGRAM = 'PROGRAM'
VAR = 'VAR'
COLON = 'COLON'
COMMA = 'COMMA'
IF = 'IF'
THEN = 'THEN'
ELSE = 'ELSE'
EQUALS = 'EQUALS'
GREATER = 'GREATER'
LESSER = 'LESSER'
GREATER_EQUALS = 'GREATER_EQUALS'
LESSER_EQUALS = 'LESSER_EQUALS'
NOT_EQUALS = 'NOT_EQUALS'
EOF = 'EOF'
