import os
import re
import toml


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


class Sectile(object):
    def __init__(self, directory):
        self.fragments_directory = directory
        self.matcher = re.compile(
            SECTILE_COMMAND,
            re.MULTILINE|re.DOTALL|re.VERBOSE
        )
        self._dimensions = self.read_dimensions_file()
        self.dimensions_list = self._dimensions['dimensions']

    def get_dimensions_list(self):
        return self.dimensions_list

    def get_dimension(self, dimension):
        if dimension in self.dimensions_list:
            if dimension in self._dimensions:
                return self._dimensions[dimension]
            else:
                return {}
        else:
            return False    # FIXME raise?

    def get_dimension_inheritance(self, dimension, key):
        dimension = self.get_dimension(dimension)
        list = []

        # see if there is a specified inheritance
        while key in dimension:
            list.append(key)
            key = dimension[key]

        # the specified key and "all" are always returned as possibilities
        list.append(key)
        list.append('all')

        return list

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

    def read_dimensions_file(self):
        try:
            content = toml.load(
                os.path.join(self.fragments_directory, 'dimensions.toml')
            )
        except FileNotFoundError:
            content = {}

        if not 'dimensions' in content:
            content["dimensions"] = []

        return content
