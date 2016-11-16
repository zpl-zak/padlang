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
from pad.libloader import LibLoader


class Interpreter(NodeVisitor):
    """
    Interprets our AST by visiting all nodes of tree.
    """
    def __init__(self, tree, parent=None):
        self.tree = tree
        self.GLOBAL_MEMORY = OrderedDict()
        self.parent = parent
        self.loader = LibLoader()
        self.types = {'INTEGER': 'int', 'STRING': 'str', 'REAL': 'float'}

    def type_check(self, name, value):
        if value is None:
            return True

        typ = self.types[name]
        return True if type(value).__name__ == typ else False

    def visit_Program(self, node):
        for x in node.imps:
            self.loader.imp(x)

        self.visit(node.block)

    def visit_VarDecl(self, node):
        self.GLOBAL_MEMORY[node.var_node.value] = node.var_node

        if node.val_node is not None:
            self.GLOBAL_MEMORY[node.var_node.value] = self.visit(node.val_node)

    @staticmethod
    def type_error(name):
        raise TypeError("Cannot assign value! Type mismatch: " + name)

    def visit_VarDeclInline(self, node):
        for decl in node.decls:
            self.visit(decl)

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_Block(self, node):
        env = self if self.parent is None else Interpreter(None, self)

        for cls in node.classes:
            env.visit(cls)

        for declaration in node.declarations:
            env.visit(declaration)

        for method in node.methods:
            env.visit(method)

        return env.visit(node.compound_statement)

    def visit_ImportDecl(self, node):
        for x in node.imps:
            self.loader.imp(x, True)

    def visit_ClassDecl(self, node):
        import pad.parse
        name = node.name.value
        self.GLOBAL_MEMORY[name] = pad.parse.Class(node.decls, node.methods)

    def visit_ClassNew(self, node):
        import copy
        import pad.parse, pad.lexer
        name = node.name.value
        cls = copy.deepcopy(self.get_var(name))

        env = Interpreter(None, self)
        for x in cls.decls:
            env.visit(x)

        for x in cls.methods:
            env.visit(x)

        try:
            ctor = pad.parse.Var(pad.lexer.Token(ID, "ctor"))
            nargs = []
            if node.args is not None:
                for x in node.args:
                    nargs.append(self.visit(x))

            ctor_call = pad.parse.MethodCall(ctor, nargs)
            env.visit(ctor_call)
        except NameError as ne:
            if node.args is not None:
                raise ne
            pass

        cls.env = env
        return cls

    def visit_String(self, node):
        return node.text

    def visit_Quoted(self, node):
        return "`"+node.text+"`"

    def visit_VarArg(self, node):
        arg = ['VARARG', node.var.value, self.visit(node.val)]
        return arg

    def visit_MethodCall(self, node, obj=None):
        import pad.parse

        try:
            method = node.name
        except Exception:
            method = node
        if type(method) is pad.parse.VarSlice:
            method = self.visit(method)
        else:
            method = None

        try:
            if method is None:
                if obj is not None and type(obj) is pad.parse.Class:
                    method = obj.env.GLOBAL_MEMORY.get(node.name.value)
                    env = obj.env
                else:
                    method = self.GLOBAL_MEMORY.get(node.name.value)
                    env = self

                while method is None and env is not None:
                    method = env.GLOBAL_MEMORY.get(node.name.value)
                    env = env.parent
        except AttributeError:
            pass

        if method is None:
            if type(node) is not pad.parse.Var:
                cargs = [self.visit(arg) for arg in node.args] if node.args is not None else ''
            else:
                cargs = node.value

            if obj is None:
                return self.loader.call(node.name.value, cargs, self)
            else:
                if type(node) is pad.parse.Var:
                    return self.loader.objcall(obj, cargs, None)
                else:
                    return self.loader.objcall(obj, node.name.value, cargs)

        currEnv = self if obj is None else obj.env
        call = Interpreter(None, currEnv)

        if type(method) is list:
            for x in method:
                a = [] if node.args is None else node.args
                b = [] if x.decl is None else x.decl

                if len(a) == len(b):
                    method = x
                    break

        for x in method.decl:
            if x.val_node is not None:
                call.GLOBAL_MEMORY[x.var_node.value] = currEnv.visit(x.val_node)

        if node.args is not None:
            i = 0
            for value in node.args:
                try:
                    visit = currEnv.visit(value)

                    if type(visit) is list:
                        if visit[0] == "VARARG":
                            call.GLOBAL_MEMORY[visit[1]] = visit[2]
                        else:
                            call.GLOBAL_MEMORY[method.decl[i].var_node.value] = visit
                    else:
                        call.GLOBAL_MEMORY[method.decl[i].var_node.value] = visit

                except Exception:
                    call.GLOBAL_MEMORY[method.decl[i].var_node.value] = value
                i += 1

        result = call.visit(method.code)

        if method.type == FUNCTION:
            return result

    def visit_ObjCall(self, node):
        import pad.parse
        this = self.visit(node.obj)
        call = node.call

        while type(call) is pad.parse.ObjCall:
            this = self.visit_MethodCall(call.obj, this)
            call = call.call

        return self.visit_MethodCall(call, this)

    def visit_Method(self, node):
        old = self.GLOBAL_MEMORY.get(node.name)

        if node.name is None:
            return node

        if old is None:
            self.GLOBAL_MEMORY[node.name] = node
        else:
            if type(old) is list:
                for x in old:
                    a = [] if node.decl is None else node.decl
                    b = [] if x.decl is None else x.decl

                    if len(a) == len(b):
                        raise NameError("Can't declare duplicate method: " + node.name)

                old.append(node)
                self.GLOBAL_MEMORY[node.name] = old
            else:
                self.GLOBAL_MEMORY[node.name] = [old, node]

    def visit_BinOp(self, node):
        try:
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
            elif node.op.type == EQUALS:
                return self.visit(node.left) == self.visit(node.right)
            elif node.op.type == NOT_EQUALS:
                return self.visit(node.left) != self.visit(node.right)
            elif node.op.type == GREATER:
                return self.visit(node.left) > self.visit(node.right)
            elif node.op.type == LESSER:
                return self.visit(node.left) < self.visit(node.right)
            elif node.op.type == LESSER_EQUALS:
                return self.visit(node.left) <= self.visit(node.right)
            elif node.op.type == GREATER_EQUALS:
                return self.visit(node.left) >= self.visit(node.right)
        except TypeError as te:
            import pad.parse
            lhs = self.visit(node.left)
            if type(lhs) is pad.parse.Class:
                import pad.lexer
                cll = pad.parse.Var(pad.lexer.Token(ID, "__" + node.op.type))
                rhs = self.visit(node.right)

                fn_call = pad.parse.MethodCall(cll, [rhs])
                return lhs.env.visit(fn_call)
            else:
                raise te

    def visit_Num(self, node):
        return node.value

    def visit_Class(self, node):
        return node

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        env = self if self.parent is None else Interpreter(None, self)

        for child in node.children[:-1]:
            env.visit(child)

        return env.visit(node.children[-1])

    def visit_CaseSwitch(self, node):
        test = self.visit(node.test)
        conds = node.conds
        alt = node.alt

        for case in conds:
            case_conds = case.cond
            res = case.cons
            xconds = []

            for cond in case_conds:
                xconds.append(self.visit(cond))

            if test in xconds:
                return self.visit(res)

            for x in xconds:
                try:
                    if test in x:
                        return self.visit(res)
                except TypeError:
                    pass

        return self.visit(alt)

    def visit_List(self, node):
        l = [self.visit(x) for x in node.list]
        return l

    def visit_Dict(self, node):
        d = {key.value: self.visit(value) for (key, value) in node.keyvals}
        return d

    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        var_left_value = self.get_var(node.left.value)

        import pad.parse
        if type(var_left_value) == pad.parse.VarRef:
            var_name = var_left_value.value

        self.set_var(var_name, var_value)

    def get_var(self, node):
        var_name = node
        symbol = self.GLOBAL_MEMORY.get(var_name)
        env = self

        try:
            while symbol is None and env is not None:
                symbol = env.GLOBAL_MEMORY.get(var_name)

                if symbol is None:
                    env = env.parent

            res = env.GLOBAL_MEMORY[var_name]
            return res
        except AttributeError:
            res = self.loader.getname(var_name)
            return res

    @staticmethod
    def error_notfound(name):
        raise NameError("Unknown variable " + name)

    def set_var(self, node, value):
        var_name = node
        var_value = value
        symbol = self.GLOBAL_MEMORY.get(var_name)
        env = self

        try:
            while symbol is None and env is not None:
                symbol = env.GLOBAL_MEMORY.get(var_name)

                if symbol is None:
                    env = env.parent

            # if type(env.GLOBAL_MEMORY[var_name].value).__name__ != type(var_value).__name__:
            #    self.type_error(var_name)

            env.GLOBAL_MEMORY[var_name] = var_value
        except AttributeError:
            self.error_notfound(var_name)

    def visit_Var(self, node):
        var_name = node.value
        res = self.get_var(var_name)

        import pad.parse
        if type(res) == pad.parse.VarRef:
            res = self.get_var(res.value)

        return res

    def visit_VarSlice(self, node):
        res = self.visit(node.var)
        acc = self.visit(node.slice)
        start = 0
        end = 1
        step = 1

        if type(acc) is list:
            if node.set is True:
                res[acc[0]] = self.visit(node.setval)
                return None
            if type(acc[0]) is str:
                return res[acc[0]]

        if len(acc) == 0:
            start = 0
            end = len(res)
        elif len(acc) > 0:
            start = acc[0]
            end = start + 1

        if len(acc) > 1:
            end = acc[1] + 1

        if len(acc) > 2:
            step = acc[2]

            if step < 1:
                step = 1

        sl = slice(start, end, step)
        nres = res[sl]

        if len(nres) == 1:
            nres = nres[0]
        if node.set is True:
            res[sl] = self.visit(node.setval)
            return None

        return nres

    def visit_VarRef(self, node):
        return node

    def visit_WhileLoop(self, node):
        cond = self.visit(node.cond)

        while cond is True:
            self.visit(node.stat)
            cond = self.visit(node.cond)

    def visit_ForLoop(self, node):
        name = node.name.value
        lst = self.visit(node.lst)
        env = Interpreter(None, self)

        for x in lst:
            env.GLOBAL_MEMORY[name] = x
            env.visit(node.stat)

    def visit_Condition(self, node):
        cons = node.cons
        alt = node.alt
        result = self.visit(node.cond)

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

