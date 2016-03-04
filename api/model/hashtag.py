import flask

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

    # DAO
    def save(self):
        query = 'insert into hashtags (entry_id, value) values (?, ?)'
        cur = flask.g.db.execute(query, [self.entry_id, self.value])
        flask.g.db.commit()
