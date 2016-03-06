import flask
import re

class TextDecorator:
    @staticmethod
    def decorate_hashtags(text):
        hashtag_matches = TextDecorator._find_hashtag_locations(text)

        for match in reversed(hashtag_matches):
            span = match.span()
            start = span[0]
            end = span[1]

            text = flask.render_template(
                'user/hashtag.html',
                prefix=text[0:start + 1], # +1 for space
                hashtag=text[start:end],
                postfix=text[end:],
                url_arg=text[start+2:end])

        return text.replace('\n', '').strip()

    @staticmethod
    def _find_hashtag_locations(text):
        pattern = re.compile(r'[^#](#[\w0-9\-_]+)\b', re.U)
        matches = list()
        for match in pattern.finditer(text):
            matches.append(match)
        return matches
