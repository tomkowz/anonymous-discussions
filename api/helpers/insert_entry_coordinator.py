from api.models.entry import Entry
from api.models.hashtag import Hashtag
from api.utils.date_utils import DateUtils
from api.utils.hashtags_finder import HashtagsFinder

class InsertEntryCoordinator:

    @staticmethod
    def insert_entry(json):
        entry = Entry.from_json(json)
        entry.timestamp = DateUtils.timestamp_for_now()
        entry.save()

        # add hashtags
        hashtags_strings = HashtagsFinder.find_hashtags(entry.content)
        for value in hashtags_strings:
            hashtag = Hashtag()
            hashtag.entry_id = entry.id
            hashtag.value = value
            hashtag.save()

        return entry
