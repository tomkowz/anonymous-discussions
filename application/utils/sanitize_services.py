import re


class Sanitize:

    @staticmethod
    def is_valid_input(text):
        valid_xss, xss_item = Sanitize.is_valid_xss_check(text)
        if valid_xss == False:
            return valid_xss, xss_item

        valid_sql, sql_item = Sanitize.is_valid_sql_check(text)
        if valid_sql == False:
            return valid_sql, sql_item

        return True, None


    @staticmethod
    def is_valid_xss_check(text):
        t = text.lower()
        blacklisted = ['<script', '</script', '<html>', '</html>',
                       'onload', 'javascript:', '<body', 'iframe',
                       '"<', '\'<', 'onmouseover', 'alert(',
                       'onerror', '<img', 'src=', 'ascript:',
                       '<style', '<meta', 'style=', 'http-equiv',
                       '<frameset', '<!--', '<!', '<object',
                       'allowscriptaccess', '</embed', 'eval', '<xml',
                       '<?xml', '<?import', '<t:set', 'cmd=', '=\"', '=\'',
                       'echo(', '<head', 'href=']

        for item in blacklisted:
            if item in t:
                return (False, item)

        return (True, None)


    @staticmethod
    def is_valid_sql_check(text):
        t = text.lower()
        blacklisted = [r'select.*\*', r'drop.*table', r'delete.*from', r'where.*=']

        for item in blacklisted:
            pattern = re.compile(item, re.U)
            result = pattern.findall(t)
            if len(result) > 0:
                return (False, result[0])

        return (True, None)
