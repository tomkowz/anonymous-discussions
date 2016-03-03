from api.model.entry import Entry

class EntryDTO:

    @staticmethod
    def to_json(entry):
        json = dict()
        json['id'] = entry.id
        json['content'] = entry.content
        json['timestamp'] = entry.timestamp
        return json

    @staticmethod
    def from_json(json):
        entry = Entry()
        entry.id = json.get('id')
        entry.content = json.get('content')
        entry.timestamp = json.get('timestamp')
        return entry
