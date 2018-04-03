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
#  LEXER                                                                      #
#                                                                             #
###############################################################################

from pad.ltypes import *


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'VAR': Token('VAR', 'VAR'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'MOD': Token('INTEGER_MOD', 'MOD'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'IF': Token('IF', 'IF'),
    'THEN': Token('THEN', 'THEN'),
    'ELSE': Token('ELSE', 'ELSE'),
    'CASE': Token('CASE', 'CASE'),
    'OF': Token('OF', 'OF'),
    'SUB': Token('SUB', 'SUB'),
    'PROCEDURE': Token('PROCEDURE', 'PROCEDURE'),
    'FUNCTION': Token('FUNCTION', 'FUNCTION'),
    'FN': Token('FN', 'FN'),
    'RET': Token('RET', 'RET'),
    'END': Token('END', 'END'),
    'IMPORT': Token('IMPORT', 'IMPORT'),
    'REQUIRE': Token('REQUIRE', 'REQUIRE'),
    'CLASS': Token('CLASS', 'CLASS'),
    'NEW': Token('NEW', 'NEW'),
    'WHILE': Token('WHILE', 'WHILE'),
    'FOR': Token('FOR', 'FOR'),
    'IN': Token('IN', 'IN'),
    'DO': Token('DO', 'DO'),
}


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, char):
        raise SyntaxError('Invalid character: ' + char)

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '$':
            self.advance()
        self.advance()  # the closing dollar sign

    def quoted(self):
        result = ''
        while self.current_char != '`':
            result += self.current_char
            self.advance()
        self.advance()
        return result

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token = Token('REAL_CONST', float(result))
        else:
            token = Token('INTEGER_CONST', int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ('_', '&', '.')):
            result += self.current_char
            self.advance()

        # Handle special occurence with END. keyword.
        if result.upper().endswith("END."):
            result = result[:-1]
            self.pos -= 1
            self.current_char = self.text[self.pos]

        if result[0] == '&':
            token = Token(REF, result[1:])
        else:
            token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result))
        return token

    def string(self):
        result = ''

        while self.current_char is not '"':
            result += self.current_char
            self.advance()

        self.advance()  # skip "
        token = Token(STRING, result)
        return token

    def peek_token(self, times):
        last = None
        pos = self.pos
        for _ in range(times):
            last = self.get_next_token()

        self.pos = pos
        self.current_char = self.text[self.pos]
        return last


    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '$':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char == '`':
                self.advance()
                return Token(GRAVE, self.quoted())

            if self.current_char == '"':
                self.advance()
                return self.string()

            if self.current_char == '{':
                self.advance()
                return Token('BEGIN', '{')

            if self.current_char == '}':
                self.advance()
                return Token('END', '}')

            if self.current_char.isalpha() or self.current_char in ('_', '&'):
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '[':
                self.advance()
                return Token(LBRACKET, '[')

            if self.current_char == ']':
                self.advance()
                return Token(RBRACKET, ']')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(EQUALS, '==')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(LESSER_EQUALS, '<=')

            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(GREATER_EQUALS, '>=')

            if self.current_char == '<' and self.peek() != '>':
                self.advance()
                return Token(LESSER, '<')

            if self.current_char == '>':
                self.advance()
                return Token(GREATER, '>')

            if self.current_char == '<' and self.peek() == '>':
                self.advance()
                self.advance()
                return Token(NOT_EQUALS, '<>')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            self.error(self.current_char)

        return Token(EOF, None)
