class Entry:
    
    @property
    def content(self):
        return self._content

    def content(self, v):
        self._content = v
