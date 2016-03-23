# -*- coding: utf-8 -*-

import time
import flask

from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from application.utils.text_decorator import TextDecorator

class PresentableObject(object):
    def __init__(self, object):
        self.object = object

class PresentableEntry(PresentableObject):

    def __init__(self, object):
        super(PresentableEntry, self).__init__(object)
        self._votes = None

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

    def _get_votes(self):
        if self._votes is None:
            self._votes = Entry.votes_with_id(self.object.id)

        return self._votes

    @property
    def votes_up(self):
        return '+{}'.format(self._get_votes()[0])

    @property
    def votes_down(self):
        return '-{}'.format(abs(self._get_votes()[1]))

class PresentableComment(PresentableObject):

    def __init__(self, object):
        super(PresentableComment, self).__init__(object)
        self._votes = None

    @property
    def created_at(self):
        return PresentableHelper.format_datetime(self.object.created_at)

    @property
    def content(self):
        text = TextDecorator.decorate_links(self.object.content)
        text = TextDecorator.decorate_hashtags(text)
        return text

    def _get_votes(self):
        if self._votes is None:
            self._votes = Comment.votes_with_id(self.object.id)

        return self._votes

    @property
    def votes_up(self):
        return '+{}'.format(self._get_votes()[0])

    @property
    def votes_down(self):
        return '-{}'.format(abs(self._get_votes()[1]))

class PresentableHelper:
    @staticmethod
    def format_datetime(datetime_obj):
        # date = time.strptime(date_as_string, '%Y-%m-%d %H:%M:%S')
        return datetime_obj.strftime('%e/%b/%y %H:%M')
