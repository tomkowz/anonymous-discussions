import datetime

from api.model.entry import Entry
from api.front.utils.hashtags import Hashtags
from api.front.utils.text_decorator import TextDecorator

class EntryViewModel:

    def __init__(self, entry):
        self._prepare(entry)

    def _prepare(self, entry):
        # Get date from timestamp
        d = datetime.datetime.fromtimestamp(entry.timestamp)
        self._date = d.strftime('%d/%m/%Y %H:%M')

        # Get content and decorate it
        hashtag_matches = Hashtags.find_hashtags(entry.content)
        self._content = TextDecorator.decorate_hashtags(hashtag_matches, entry.content)

    @property
    def date(self):
        return self._date

    @property
    def content(self):
        return self._content
