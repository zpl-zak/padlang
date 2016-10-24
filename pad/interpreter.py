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
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

from collections import OrderedDict

from pad.ltypes import *
from pad.walker import NodeVisitor


class Interpreter(NodeVisitor):
    def __init__(self, tree, parent=None):
        self.tree = tree
        self.GLOBAL_MEMORY = OrderedDict()
        self.parent = parent

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_VarDecl(self, node):
        self.GLOBAL_MEMORY[node.var_node.value] = node.var_node

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_Block(self, node):
        #self.child = table = SymbolTableBuilder(self.symtab)

        for declaration in node.declarations:
            self.visit(declaration)

        for method in node.methods:
            self.visit(method)

        return self.visit(node.compound_statement)

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_MethodCall(self, node):
        method = self.GLOBAL_MEMORY.get(node.name.value)

        if method is None:
            raise Exception("Undefined method " + node.name.value)

        call = Interpreter(None, self)

        i = 0

        for value in node.args:
            call.GLOBAL_MEMORY[method.decl[i].var_node.value] = value
            i += 1

        result = call.visit(method.code)

        if method.type == FUNCTION:
            return result

    def visit_Method(self, node):
        self.GLOBAL_MEMORY[node.name] = node

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == INTEGER_MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children[:-1]:
            self.visit(child)

        return self.visit(node.children[-1])

    def visit_CaseSwitch(self, node):
        test = self.visit(node.test)
        conds = node.conds
        alt = node.alt

        met = False
        for case in conds:
            case_conds = case.cond
            res = case.cons
            for cond in case_conds:
                if self.visit(cond) == test:
                    self.visit(res)
                    met = True

        if met is False:
            self.visit(alt)


    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        symbol = self.GLOBAL_MEMORY.get(var_name)
        env = self

        while symbol is None and env.parent is not None:
            env = env.parent
            symbol = env.GLOBAL_MEMORY.get(var_name)

        env.GLOBAL_MEMORY[var_name] = var_value


    def visit_Var(self, node):
        var_name = node.value
        symbol = self.GLOBAL_MEMORY.get(var_name)
        env = self

        while symbol is None and env.parent is not None:
            env = env.parent
            symbol = env.parent.GLOBAL_MEMORY.get(var_name)

        try:
            return self.visit(symbol)
        except Exception:
            return symbol

    def visit_Condition(self, node):
        left = node.left
        op = node.op
        right = node.right
        cons = node.cons
        alt = node.alt
        result = False
        if op.type == EQUALS:
            result = self.visit(left) == self.visit(right)
        if op.type == NOT_EQUALS:
            result = self.visit(left) != self.visit(right)
        if op.type == GREATER:
            result = self.visit(left) > self.visit(right)
        if op.type == LESSER:
            result = self.visit(left) < self.visit(right)
        if op.type == LESSER_EQUALS:
            result = self.visit(left) <= self.visit(right)
        if op.type == GREATER_EQUALS:
            result = self.visit(left) >= self.visit(right)

        if result is True:
            self.visit(cons)
        else:
            self.visit(alt)

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)

