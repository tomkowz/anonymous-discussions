import re

class Hashtags:

    @staticmethod
    def find_hashtags(text):
        pattern = re.compile(r'(#.+?\b)')
        matches = list()
        for match in pattern.finditer(text):
            matches.append(match)
        return matches
