"""
  Copyright 2016 Dominik Madarasz
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

###############################################################################
#                                                                             #
#  TOKEN TYPES                                                                #
#                                                                             #
###############################################################################

# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER = 'INTEGER'
REAL = 'REAL'
STRING = 'STRING'
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
LBRACKET = 'LBRACKET'
RBRACKET = 'RBRACKET'
ID = 'ID'
REF = 'REF'
ASSIGN = 'ASSIGN'
BEGIN = 'BEGIN'
END = 'END'
OF = 'OF'
CASE = 'CASE'
FUNCTION = 'FUNCTION'
FN = 'FN'
SUB = 'SUB'
PROCEDURE = 'PROCEDURE'
SEMI = 'SEMI'
DOT = 'DOT'
PROGRAM = 'PROGRAM'
VAR = 'VAR'
RET = 'RET'
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
