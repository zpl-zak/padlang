class Print(object):
    def __init__(self):
        pass

    def call(self, args):
        print(args[0])


class Input(object):
    def call(self, args):
        return input(args)