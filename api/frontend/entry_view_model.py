import datetime

from api.frontend.entry_presentation import EntryPresentation
from api.models.entry import Entry
from api.utils.hashtags_finder import HashtagsFinder

class EntryViewModel:

    def __init__(self, entry):
        self._prepare(entry)

    def _prepare(self, entry):
        # Get date from timestamp
        d = datetime.datetime.fromtimestamp(entry.timestamp)
        self._date = d.strftime('%d/%m/%Y %H:%M')

        # Get content and decorate it
        self._content = EntryPresentation.decorate_text(entry.content)

    @property
    def date(self):
        return self._date

    @property
    def content(self):
        return self._content
