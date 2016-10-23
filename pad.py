""" PadLang (c) Dominik Madarasz <zaklaus@madaraszd.net> """

###############################################################################
#                                                                             #
#  LOADER                                                                     #
#                                                                             #
###############################################################################

from lexer import Lexer
from parse import Parser
from symtable import SymbolTableBuilder
from interpreter import Interpreter


def main():
    import sys
    text = open(sys.argv[1], 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SymbolTableBuilder()
    symtab_builder.visit(tree)
    print('')
    print('Symbol Table contents:')
    print(symtab_builder.symtab)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()

    print('')
    print('Run-time GLOBAL_MEMORY contents:')
    for k, v in sorted(interpreter.GLOBAL_MEMORY.items()):
        print('%s = %s' % (k, v))


if __name__ == '__main__':
    main()
