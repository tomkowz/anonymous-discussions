# -*- coding: utf-8 -*-
import flask, re
from application.mod_api.utils_hashtags import HashtagsUtils


class TextDecorator:

    @staticmethod
    def decorate_hashtags(text):
        matches = HashtagsUtils.find_hashtags_locations(text)
        for match in reversed(matches):
            start, end = match.span()
            text = flask.render_template(
                'web/hashtag.html',
                prefix=text[0:start],
                hashtag=text[start:end],
                postfix=text[end:],
                url_arg=text[start+1:end])

        return text


    @staticmethod
    def decorate_links(text):
        for match in reversed(TextDecorator._find_link_locations(text)):
            start, end = match.span()
            text = flask.render_template(
                'web/link.html',
                prefix=text[0:start],
                link=text[start:end],
                postfix=text[end:])

        return text


    @staticmethod
    def _find_link_locations(text):
        # http://stackoverflow.com/a/6883094/1046965
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.U)
        return [x for x in pattern.finditer(text)]
