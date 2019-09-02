import os
import re
# import toml


SECTILE_COMMAND = r"""
    ^

    # grab what comes before the sectile command
    (?P<before> .* )

    # the sectile command, grab the name of the inserted file
    \<\% \s* sectile \s+ insert \s+ (?P<insert> .*? ) \s* \%\>

    # grab what comes after the sectile command
    (?P<after> .* )

    $
"""


class Sectile(object):
    def __init__(self, directory):
        self.fragments_directory = directory
        self.matcher = re.compile(
            SECTILE_COMMAND,
            re.MULTILINE|re.DOTALL|re.VERBOSE
        )

    def expand(self, string):
        matches = re.search(self.matcher, string)
        expanded = string

        if matches is not None:
            if matches.group('insert'):
                insert = self.get_file(matches.group('insert'))
                expanded = (
                    matches.group('before')
                    + insert
                    + matches.group('after')
                )

        return expanded

    def get_file(self, file):
        found_file = os.path.join(
            self.fragments_directory,
            file
        )
        try:
            with open(found_file) as ff:
                return ff.read()
        except FileNotFoundError:
            return '' 
