import itertools
import os
import re
import toml


SECTILE_COMMAND = r"""
    ^

    # grab what comes before the sectile command
    (?P<before> .*? )

    # inspect leading whitespace
    ( (?P<nlbefore> \n ) [ \t]* )?

    # the sectile command, grab the name of the inserted file
    \[\[ \s* sectile \s+ insert \s+ (?P<insert> .*? ) \s* \]\]

    # inspect trailing whitespace
    ( [ \t]* (?P<nlafter> \n ) )?

    # grab what comes after the sectile command
    (?P<after> .* )

    $
"""


class Sectile(object):
    def __init__(self, directory, dimensions=[]):
        self.fragments_directory = directory
        self.matcher = re.compile(
            SECTILE_COMMAND,
            re.MULTILINE|re.DOTALL|re.VERBOSE
        )
        self._dimensions = self.build_dimensions(dimensions)
        self.dimensions_list = []
        for key in self._dimensions:
            self.dimensions_list.append(key)

    def generate_target(self, target, base_fragment, **kwargs):
        base = self.get_fragment(base_fragment, target, **kwargs)
        if not base:
            raise FileNotFoundError
        return self.expand(base, target, **kwargs)

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

    def expand(self, string, path, **kwargs):
        matches = re.search(self.matcher, string)
        expanded = string

        # FIXME check for an infinite loop
        if matches is not None:
            if matches.group('insert'):
                insert = self.get_fragment(matches.group('insert'), path, **kwargs)
                if not insert:
                    insert = ''

                # strip trailing whitespace from the text to be inserted
                # if the command was followed by more text
                if matches.group('nlafter') != '\n':
                    insert = insert.rstrip()

                if matches.group('nlafter') == '\n' and not insert.endswith('\n'):
                    insert = insert + '\n'

                if matches.group('nlbefore') == '\n':
                    insert = '\n' + insert

                expanded = (
                    matches.group('before')
                    + insert
                    + matches.group('after')
                )
            return self.expand(expanded, path, **kwargs)
        else:
            return string

    def get_fragment(self, fragment, path, **kwargs):
        for path in self.get_fragment_paths(fragment, path, **kwargs):
            target = os.path.join(self.fragments_directory, path)
            if os.path.exists(target):
                with open(target) as file:
                    return file.read()
        return None

    def get_fragment_paths(self, fragment, path, **kwargs):
        paths = self.split_path(path)

        dimension_possibilities = []
        for dimension in self.get_dimensions_list():
            if dimension in kwargs:
                dimension_possibilities.append(
                    self.get_dimension_inheritance(dimension, kwargs[dimension])
                )
            else:
                dimension_possibilities.append(['all'])

        dimension_paths = []
        if len(dimension_possibilities):
            for combo in itertools.product(*dimension_possibilities):
                # ignore when all dimensions are "all" (the generic case)
                if combo.count('all') != len(combo):
                    dimension_paths.append(os.path.join(*combo))

        fragment_paths = []
        for path in paths:
            for dimension_path in dimension_paths:
                fragment_paths.append(os.path.join(dimension_path, path, fragment))
        for path in paths:
            fragment_paths.append(os.path.join('default', path, fragment))

        return fragment_paths

    def split_path(self, path):
        if path.find('/') >= 0:
            path = os.path.normpath(path).lstrip('/')
        paths = []
        paths.append(path)
        (head, tail) = os.path.split(path)
        while tail:
            paths.append(head)
            (head, tail) = os.path.split(head)
        return paths

    def build_dimensions(self, dimensions):
        if not dimensions:
            try:
                dimensions = toml.load(
                    os.path.join(self.fragments_directory, 'dimensions.toml')
                )
            except FileNotFoundError:
                dimensions = {}
        return dimensions
