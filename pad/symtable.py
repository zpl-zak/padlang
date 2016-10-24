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
#  SYMBOLS and SYMBOL TABLE                                                   #
#                                                                             #
###############################################################################

from collections import OrderedDict

from pad.walker import NodeVisitor
from pad.ltypes import *


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class MethodSymbol(Symbol):
    def __init__(self, name, syms, type_spec, type):
        super(MethodSymbol, self).__init__(name, type)
        self.syms = syms
        self.type_spec = type_spec

    def __str__(self):
        a = self.syms.debug_dump()
        return '<METHOD {name}:{type} ({mem})>'.format(name=self.name, type=self.type, mem=a)

    __repr__ = __str__


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self, parent=None):
        self.symbols = OrderedDict()
        self._init_builtins()
        self.parent = parent

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self.symbols.values()]
        )
        return s

    __repr__ = __str__

    def define(self, symbol):
        print('Define: %s' % symbol)
        self.symbols[symbol.name] = symbol

    def set(self, name, value):
        print('Define: %s' % name)
        self.symbols[name] = value

    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self.symbols.get(name)
        if symbol is None and self.parent is not None:
            symbol = self.parent.lookup(name)

        print(symbol)
        return symbol


class SymbolTableBuilder(NodeVisitor):
    """
    Takes an ADT (Abstract Data Tree) and checks all nodes for undeclared variables usage, type-checking...
    """
    def __init__(self, parent=None):
        self.symtab = SymbolTable(parent)
        self.child = None

    def debug_dump(self):
        s = '(' + str(self.symtab) + ')'

        if self.child is not None:
            s += '\n(' + self.child.debug_dump() + ')'

        return s

    def visit_Block(self, node):
        #self.child = table = SymbolTableBuilder(self.symtab)

        for declaration in node.declarations:
            self.visit(declaration)

        for method in node.methods:
            self.visit(method)

        self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Method(self, node):
        self.child = table = SymbolTableBuilder(self.symtab)

        for decl in node.decl:
            table.visit(decl)

        method = MethodSymbol(node.name, table, None, PROCEDURE)
        self.symtab.define(method)

        table.visit(node.code)

    def visit_MethodCall(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_CaseSwitch(self, node):
        self.visit(node.test)
        conds = node.conds
        alt = node.alt

        for case in conds:
            case_conds = case.cond
            res = case.cons
            for cond in case_conds:
                self.visit(cond)
                self.visit(res)

        self.visit(alt)

    def visit_NoOp(self, node):
        pass

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)

    def visit_VarDeclInline(self, node):
        for decl in node.decls:
            self.visit(decl)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

        self.visit(node.right)

    def visit_Condition(self, node):
        self.visit(node.cons)
        self.visit(node.alt)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)

        if var_symbol is None:
            raise NameError(repr(var_name))

