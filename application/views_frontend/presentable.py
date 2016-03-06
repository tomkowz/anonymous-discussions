# -*- coding: utf-8 -*-

import datetime
import flask

from application.models.entry import Entry
from application.models.comment import Comment
from application.utils.text_decorator import TextDecorator

class PresentableHelper:
    @staticmethod
    def format_date_from_timestamp(timestamp):
        d = datetime.datetime.fromtimestamp(timestamp)
        return d.strftime('%e/%b/%y %H:%M')

class PresentableObject:
    def __init__(self, object):
        self._object = object

    @property
    def object(self):
        return self._object

class PresentableEntry(PresentableObject):
    @property
    def date(self):
        return PresentableHelper.format_date_from_timestamp(self.object.timestamp)

    @property
    def content(self):
        text = TextDecorator.decorate_links(self.object.content)
        text = TextDecorator.decorate_hashtags(text)
        return text

    @property
    def comments_count(self):
        return Comment.get_comments_count_with_entry_id(self.object.id)

class PresentableComment(PresentableObject):
    @property
    def date(self):
        return PresentableHelper.format_date_from_timestamp(self.object.timestamp)

    @property
    def content(self):
        return TextDecorator.decorate_hashtags(self.object.content)
