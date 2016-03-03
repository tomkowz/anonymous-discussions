class TextDecorator:

    @staticmethod
    def decorate_hashtags(matches, text):
        for match in reversed(matches):
            span = match.span()
            start = span[0]
            end = span[1]

            text = text[0:start] + \
                   '<span class="hashtag">' + \
                   text[start:end] + \
                   '</span>' + \
                   text[end:]
        return text
