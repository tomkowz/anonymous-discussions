# -*- coding: utf-8 -*-
class TextExcerpt:

    @staticmethod
    def excerpt_for_url(text, length=70):
        """Takes text and prepare excerpt from it that will be inserted into
        part of url. No special characters, only alphanumeric and dashes.
        """

        text = text.strip()
        text = text.replace(' ', '-')
        text = text.lower()

        allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzęóąśłżźćń-'
        text = filter(lambda x: x in allowed_chars, text)

        return text[:length]
