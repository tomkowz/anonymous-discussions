import datetime

from api.dao.entry_dao import EntryDAO
from api.dao.hashtag_dao import HashtagDAO
from api.dto.entry_dto import EntryDTO
from api.model.entry import Entry
from api.model.hashtag import Hashtag
from api.utils.hashtags import Hashtags

class InsertEntryCoordinator:

    @staticmethod
    def insert_entry(json):
        entry = EntryDTO.from_json(json)

        # timestamp for NOW
        now = datetime.datetime.utcnow()
        epoch = datetime.datetime(1970,1,1)
        timestamp = (now - epoch).total_seconds()
        entry.timestamp = timestamp

        EntryDAO.insert(entry)

        # add hashtags
        hashtags_strings = Hashtags.find_hashtags(entry.content)
        for value in hashtags_strings:
            hashtag = Hashtag()
            hashtag.entry_id = entry.id
            hashtag.value = value
            HashtagDAO.insert(hashtag)

        return entry
