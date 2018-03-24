class Test1(object):
    def call(self, args):
        return 1


class Test2(object):
    def call(self, args):
        return 2


class TestFoo(object):
    def __init__(self):
        self.bar = 42


class TestBar(object):
    def __init__(self):
        self.foo = TestFoo()

    def barbar(self):
        return self.foo