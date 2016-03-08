# -*- coding: utf-8 -*-

import time
import flask

from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from application.utils.text_decorator import TextDecorator

class PresentableObject:
    def __init__(self, object):
        self.object = object

class PresentableEntry(PresentableObject):
    @property
    def created_at(self):
        return PresentableHelper.format_datetime(self.object.created_at)

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
    def created_at(self):
        return PresentableHelper.format_datetime(self.object.created_at)

    @property
    def content(self):
        text = TextDecorator.decorate_links(self.object.content)
        text = TextDecorator.decorate_hashtags(text)
        return text

class PresentableHelper:
    @staticmethod
    def format_datetime(datetime_obj):
        # date = time.strptime(date_as_string, '%Y-%m-%d %H:%M:%S')
        return datetime_obj.strftime('%e/%b/%y %H:%M')
