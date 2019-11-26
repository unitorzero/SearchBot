from sqlalchemy import func, literal_column


def json_agg(table):
    return func.json_agg(literal_column('"' + table.name + '"'))


class PaginateQuery:
    def __init__(self, query, paginate_column, page_len=5, first=0, last=0, order_desc=False):
        self.query = query
        self.column = paginate_column
        self.page_len = page_len
        self.first = first
        self.last = last
        self.order_desc = order_desc

    def next(self, first=False):
        filters = []
        if not first:
            filters.append(self.column > self.last if not self.order_desc else self.column < self.last)
        items = self.query.filter(*filters).order_by(self.column if not self.order_desc
                                                     else self.column.desc()).limit(self.page_len).all()

        return {
            'type': 'next',
            'result': items,
            'page_len': self.page_len,
            'result_count': len(items)
        }

    def prev(self):
        items = self.query.filter(self.column < self.first
                                  if not self.order_desc
                                  else self.column > self.first).order_by(self.column.desc()
                                                                          if not self.order_desc
                                                                          else self.column).limit(self.page_len).all()
        items.reverse()

        return {
            'type': 'prev',
            'result': items,
            'page_len': self.page_len,
            'result_count': len(items)
        }
