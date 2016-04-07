import re


class MentionsUtils:

    @staticmethod
    def find_mentions_locations(text):
        pattern = re.compile(r'@[op|OP|0-9]+', re.U)
        return [m for m in pattern.finditer(text)]


    @staticmethod
    def get_mentions_from_text(text):
        result = list()
        for match in MentionsUtils.find_mentions_locations(text):
            start, end = match.span()
            mention = text[start+1:end]
            result.append(mention)
        return result
