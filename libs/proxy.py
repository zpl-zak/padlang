def extern(callback, env):
    return CallBack(callback, env)


class CallBack(object):
    def __init__(self, method, env):
        self.node = method
        self.call = env

    def __call__(self, *args, **kwargs):
        if args is not None:
            i = 0
            for value in args:
                self.call.GLOBAL_MEMORY[self.node.decl[i].var_node.value] = value
                i += 1

        for x in self.node.decl:
            if x.val_node is not None:
                self.call.GLOBAL_MEMORY[x.var_node.value] = self.call.visit(x.val_node)

        self.call.visit(self.node.code)
