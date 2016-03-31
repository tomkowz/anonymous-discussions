import flask

from application import app
from math import ceil


def url_for_other_page(page):
    args = flask.request.view_args.copy()
    args['page'] = page
    return flask.url_for(flask.request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page


class Pagination:

    def __init__(self, page, items_per_page, total_count):
        self.page = page
        self.items_per_page = items_per_page
        self.total_count = total_count


    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.items_per_page)))


    @property
    def has_prev(self):
        return self.page > 1


    @property
    def has_next(self):
        return self.page < self.pages


    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               num > self.pages - right_edge or \
              (num > self.page - left_current - 1 and \
               num < self.page + right_current):

               if last + 1 != num:
                   yield None
               yield num
               last = num
