# -*- coding: utf-8 -*-

import datetime
import flask

from api.models.entry import Entry
from api.utils.text_decorator import TextDecorator

class PresentableEntry:

    def __init__(self, entry):
        self._prepare(entry)

    def _prepare(self, entry):
        self._id = entry.id
        # Get date from timestamp
        d = datetime.datetime.fromtimestamp(entry.timestamp)
        self._date = d.strftime('%d/%m/%Y %H:%M')

        # Get content and decorate it
        self._content = TextDecorator.decorate_hashtags(entry.content)

    @property
    def date(self):
        return self._date

    @property
    def content(self):
        return self._content

    @property
    def id(self):
        return self._id
