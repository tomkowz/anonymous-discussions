# -*- coding: utf-8 -*-

import re

class HashtagsFinder:

    @staticmethod
    def find_hashtag_locations(text):
        pattern = re.compile(r'[^#](#[\w0-9\-_]+)\b', re.U)
        matches = list()
        for match in pattern.finditer(text):
            matches.append(match)
        return matches

    @staticmethod
    def find_hashtags(text):
        pattern = re.compile(r'[^#]#([\w0-9\-_]+)\b', re.U)
        return pattern.findall(text)
