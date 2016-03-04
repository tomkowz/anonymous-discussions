class Entry:

    @property
    def id(self):
        return self._id

    def id(self, v):
        self._id = v

    @property
    def content(self):
        return self._content

    def content(self, v):
        self._content = v

    @property
    def timestamp(self):
        return self._timestamp

    def timestamp(self, v):
        self._timestamp = v

    # DTO
    def to_json(self):
        json = dict()
        json['id'] = self.id
        json['content'] = self.content
        json['timestamp'] = self.timestamp
        return json

    @staticmethod
    def from_json(json):
        entry = Entry()
        entry.id = json.get('id')
        entry.content = json.get('content')
        entry.timestamp = json.get('timestamp')
        return entry
