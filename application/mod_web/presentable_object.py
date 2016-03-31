# -*- coding: utf-8 -*-
import flask, re, time, urllib

from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_comment import Comment, CommentDAO
from application.mod_api.models_user_notification import UserNotification
from application.utils.text_decorator import TextDecorator
from application.utils.text_excerpt import TextExcerpt


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
        text = re.sub('\r\n', '<br/>', text)
        return text


    @property
    def excerpt_for_url(self):
        return TextExcerpt.excerpt_for_url(text=self.object.content, length=70)

    @property
    def see_link(self):
        return urllib.unquote(flask.url_for('single_entry',
            entry_id=self.object.id,
            excerpt=self.excerpt_for_url))


    @property
    def comments_count(self):
        return self.object.comments_count


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
        text = re.sub('\r\n', '<br/>', text)
        return text


class PresentablePopularHashtag(PresentableObject):

    @property
    def content(self):
        name = '#' + self.object.name
        text = TextDecorator.decorate_links(name)
        text = TextDecorator.decorate_hashtags(name)
        return text


class PresentableRecommendedHashtag(PresentablePopularHashtag):
    pass


class PresentableUserNotification(PresentableObject):

    @property
    def content(self):
        return self.object.content


    @property
    def created_at(self):
        return PresentableHelper.format_datetime(self.object.created_at)


    @property
    def see_link(self):
        return flask.url_for('single_entry', entry_id=self.object.object_id)

class PresentableHelper:

    @staticmethod
    def format_datetime(datetime_str):
        d = time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        iso = time.strftime('%e/%b/%y %H:%M', d)
        return iso
