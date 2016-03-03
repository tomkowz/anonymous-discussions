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
