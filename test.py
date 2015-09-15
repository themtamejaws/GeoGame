class Test(object):

    def __init__(self):
        self.a = 2
        self.b = 4

class Test2(object):

    def __init__(self):

        c = Test()
        self.to_string(c)

    def to_string(self, c):
        members = [attr for attr in dir(c) if not callable(attr) and not attr.startswith("__")]
        setattr(c, members[0], 3)
        print c.a


cls = Test2()
