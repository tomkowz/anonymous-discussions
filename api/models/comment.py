class Comment:

    @property
    def entry_id(self):
        return self._entry_id

    def entry_id(self, v):
        return self._entry_id = v

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
    
