import datetime

class DateUtils:

    @staticmethod
    def timestamp_for_now():
        now = datetime.datetime.utcnow()
        epoch = datetime.datetime(1970,1,1)
        timestamp = (now - epoch).total_seconds()
        return timestamp
