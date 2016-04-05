import re


class HashtagsUtils:

    @staticmethod
    def find_hashtags_locations(text):
        pattern = re.compile(r'(#[\w0-9\-_]+)\b', flags=re.UNICODE)
        return [m for m in pattern.finditer(text)]


    @staticmethod
    def get_hashtags_from_text(text):
        result = list()
        for match in HashtagsUtils.find_hashtags_locations(text):
            start, end = match.span()
            hashtag = text[start+1:end]
            result.append(hashtag)
        return result


    @staticmethod
    def convert_hashtags_to_lowercase(text):
        matches = HashtagsUtils.find_hashtags_locations(text)
        if len(matches) == 0:
            return text

        output = ""
        cur_pos = 0
        for match in HashtagsUtils.find_hashtags_locations(text):
            start, end = match.span()
            output += text[cur_pos:start]
            output += text[start:end].lower()
            cur_pos = end

        if cur_pos < len(text):
            # go back one index because there was no more text to copy.
            # cur_pos -= 1
            # copy everything from cur_pos to end of the string
            output += text[cur_pos:len(text)]

        return output
