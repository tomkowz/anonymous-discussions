import flask

from api.utils.hashtags_finder import HashtagsFinder

class EntryPresentation:

    @staticmethod
    def decorate_text(text):
        hashtag_matches = HashtagsFinder.find_hashtag_locations(text)

        for match in reversed(hashtag_matches):
            span = match.span()
            start = span[0]
            end = span[1]

            # +1 for space
            text = flask.render_template('hashtag.html',
                                         prefix=text[0:start + 1],
                                         hashtag=text[start:end],
                                         postfix=text[end:],
                                         url_arg=text[start+2:end])
        return text
