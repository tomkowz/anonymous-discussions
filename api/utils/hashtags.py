import re

class Hashtags:

    @staticmethod
    def find_hashtag_locations(text):
        pattern = re.compile(r'[^#](#[a-zA-Z0-9\-_]+)\b')
        matches = list()
        for match in pattern.finditer(text):
            matches.append(match)
        return matches

    @staticmethod
    def find_hashtags(text):
        pattern = re.compile(r'[^#]#([a-zA-Z0-9\-_]+)\b')
        return pattern.findall(text)
