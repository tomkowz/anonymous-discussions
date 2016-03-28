import flask
import re


class TextDecorator:

    @staticmethod
    def decorate_hashtags(text):
        for match in reversed(TextDecorator._find_hashtag_locations(text)):
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
    def get_hashtags_from_text(text):
        result = list()
        for match in TextDecorator._find_hashtag_locations(text):
            start, end = match.span()
            result.append(text[start+1:end])
        return result


    @staticmethod
    def _find_hashtag_locations(text):
        pattern = re.compile(r'(#[\w0-9\-_]+)\b', re.U)
        return [m for m in pattern.finditer(text)]


    @staticmethod
    def _find_link_locations(text):
        # http://stackoverflow.com/a/6883094/1046965
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.U)
        return [x for x in pattern.finditer(text)]
