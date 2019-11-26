class Join:
    def __init__(self, join_obj, on, isouter=False):
        self.join_obj = join_obj
        self.mapper = self.join_obj.__mapper__.class_
        self.on = on
        self.isouter = isouter

    def to(self, query):
        return query.join(self.join_obj, self.on, isouter=self.isouter)

