class Hashtag:

    @property
    def entry_id(self):
        return self._entry_id

    def entry_id(self, v):
        self._entry_id = v

    @property
    def value(self):
        return self._value

    def value(self, v):
        self._value = v
