from sqlalchemy import String, any_, cast


class Filter:
    def __init__(self, filter_obj):
        self.filter_obj = filter_obj
        self.value = None

    def generate(self, value):
        if isinstance(value, list):
            return self.filter_obj.in_(value)
        return self.filter_obj == str(value)


class FilterILike(Filter):
    def __init__(self, filter_obj):
        super().__init__(filter_obj)
        if 'NUMERIC' in str(self.filter_obj.type):
            self.filter_obj = cast(self.filter_obj, String)

    def generate(self, value):
        if isinstance(value, list):
            return self.filter_obj.ilike(any_(value))
        return self.filter_obj.ilike(value)
