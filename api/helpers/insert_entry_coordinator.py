import datetime

from api.model.entry import Entry
from api.dao.entry_dao import EntryDAO
from api.dto.entry_dto import EntryDTO

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
        return entry
