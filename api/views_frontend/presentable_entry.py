import datetime
import flask

from api.models.entry import Entry
from api.utils.hashtags_finder import HashtagsFinder

class PresentableEntry:

    def __init__(self, entry):
        self._prepare(entry)

    def _prepare(self, entry):
        self._id = entry.id
        # Get date from timestamp
        d = datetime.datetime.fromtimestamp(entry.timestamp)
        self._date = d.strftime('%d/%m/%Y %H:%M')

        # Get content and decorate it
        self._content = self._decorate_text(entry.content)

    def _decorate_text(self, text):
        hashtag_matches = HashtagsFinder.find_hashtag_locations(text)

        for match in reversed(hashtag_matches):
            span = match.span()
            start = span[0]
            end = span[1]

            text = flask.render_template(
                'hashtag.html',
                prefix=text[0:start + 1], # +1 for space
                hashtag=text[start:end],
                postfix=text[end:],
                url_arg=text[start+2:end])

        return text

    @property
    def date(self):
        return self._date

    @property
    def content(self):
        return self._content

    @property
    def id(self):
        return self._id
