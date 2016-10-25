class Str(object):
    def call(self, args):
        return str(args[0])


class Int(object):
    def call(self, args):
        return int(args[0])


class Float(object):
    def call(self, args):
        return float(args[0])

