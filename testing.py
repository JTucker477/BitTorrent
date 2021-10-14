


class myClass(object):
    def __init__(self, attr):
        self.attr = attr
        self.other = None
objs = [myClass(i) for i in range(10)]

attr=[o.attr for o in objs]
print(attr)
# attr=(o.attr for o in objsm)