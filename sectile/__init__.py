import re


SECTILE_COMMAND = r"""
    ^

    # grab what comes before the sectile command
    (?P<before> .* )

    # the sectile command, grab the name of the inserted file
    \[\[ \s* sectile \s+ insert \s+ (?P<insert> .*? ) \s* \]\]

    # grab what comes after the sectile command
    (?P<after> .* )

    $
"""

INSERT = 'INSERTED TEXT'


class Sectile(object):
    def __init__(self):
        self.matcher = re.compile(
            SECTILE_COMMAND,
            re.MULTILINE|re.DOTALL|re.VERBOSE
        )

    def expand(self, string):
        matches = re.search(self.matcher, string)
        expanded = string

        if matches is not None:
            if matches.group('insert'):
                expanded = matches.group('before') + INSERT + matches.group('after')

        return expanded
