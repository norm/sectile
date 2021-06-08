import itertools
import os
from pathlib import Path
import re
import toml


RESERVED_DIMENSIONS = (
    'dimension',
    'dimensions',
    'intl',
    'sectile',
    'targets',
    'paths',
    'path'
)
RESERVED_DIMENSION_INSTANCES = (
    'generic',
    'default',
    'all',
)
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
    def __init__(
        self,
        *,
        fragments='',
        destination=None,
        dimensions=[],
        targets=[],
    ):
        self.fragments_directory = fragments
        self.destination_directory = destination
        self.matcher = re.compile(
            SECTILE_COMMAND,
            re.MULTILINE|re.DOTALL|re.VERBOSE
        )
        self._dimensions = self.build_dimensions(dimensions)
        self.dimensions_list = []
        for key in self._dimensions:
            self.dimensions_list.append(key)
        self._targets = self.build_targets(targets)
        self.all_dimension_instances = []
        for dimension in self.get_dimensions_list():
            self.all_dimension_instances.append(
                self.get_dimension_instances(dimension)
            )

    def generate_all_targets(self):
        dimensions = self.get_dimensions_list()
        for combo in itertools.product(*self.all_dimension_instances):
            args = {}
            for i, instance in enumerate(combo):
                args[dimensions[i]] = instance

            skips = self._targets['dimensions']['ignore']
            for target in self._targets:
                if target == 'dimensions':
                    continue

                dimension = '/'.join(combo)
                skip_target = False
                for skip in skips:
                    if dimension.startswith(skip):
                        skip_target = True

                if skip_target:
                    continue

                target_file = os.path.join(
                    self.destination_directory,
                    *combo, 
                    self._targets[target]['target'],
                )
                (content, fragments) = self.generate(
                    self._targets[target]['target'],
                    self._targets[target]['base'],
                    **args
                )
                _directory = os.path.dirname(target_file)
                if not os.path.isdir(_directory):
                    os.makedirs(_directory)
                with open(target_file, 'w') as handle:
                    handle.write(content)

    def generate(self, target, base_fragment, **kwargs):
        match = self.get_matching_fragment(base_fragment, target, **kwargs)
        if not match['found']:
            raise FileNotFoundError(base_fragment)

        fragment_file = self.get_fragment_file(match['found'])
        (content, fragments) = self.expand(
            fragment_file,
            target,
            1,
            **kwargs,
        )
        fragments = [{
                'dimensions': match['dimensions'],
                'file': base_fragment,
                'found': match['found'],
                'fragment': fragment_file,
                'depth': 0
            }] + fragments
        return content, fragments

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
 
    def get_dimension_instances(self, dimension):
        instances = {}
        dimension = self.get_dimension(dimension)
        for key in dimension:
            instances[key] = 1
            instances[dimension[key]] = 1
        instances['all'] = 1
        return list(instances)

    def expand(self, string, path, depth=1, **kwargs):
        expanded = string
        fragments = []

        # FIXME check for an infinite loop
        matches = re.search(self.matcher, string)
        while matches is not None:
            insert = matches.group('insert')
            match = self.get_matching_fragment(insert, path, **kwargs)
            if match['found']:
                replacement = self.get_fragment_file(match['found'])
                fragments.append({
                        'dimensions': match['dimensions'],
                        'file': insert,
                        'found': match['found'],
                        'fragment': replacement,
                        'depth': depth,
                    })
                (insertion, matched) = self.expand(
                    replacement, path, depth+1, **kwargs)
                if matched:
                    fragments += matched
            else:
                fragments.append({
                        'dimensions': match['dimensions'],
                        'file': insert,
                        'found': None,
                        'fragment': '',
                        'depth': depth,
                    })
                insertion = ''

            # strip trailing whitespace from the insertion
            # if the command was followed by more text
            if matches.group('nlafter') != '\n':
                insertion = insertion.rstrip()

            if matches.group('nlafter') == '\n' and not insertion.endswith('\n'):
                insertion = insertion + '\n'

            if matches.group('nlbefore') == '\n':
                insertion = '\n' + insertion

            string = (
                matches.group('before')
                + insertion
                + matches.group('after')
            )
            matches = re.search(self.matcher, string)

        return string, fragments

    def get_matching_fragment(self, fragment, path, **kwargs):
        match = {
            'found': None,
            'dimensions': {},
        }
        dimensions = self.get_dimensions_list()
        for path in self.get_fragment_paths(fragment, path, **kwargs):
            target = os.path.join(self.fragments_directory, path)
            if os.path.exists(target):
                match['found'] = path
                ppath = Path(path)
                if ppath.parts[0] == 'default':
                    match['dimensions']['path'] = os.path.join(*ppath.parts[1:])
                    for dimension in dimensions:
                        match['dimensions'][dimension] = 'all'
                else:
                    for dimension in dimensions:
                        match['dimensions'][dimension] = ppath.parts[0]
                        ppath = Path(os.path.join(*ppath.parts[1:]))    # FIXME
                    match['dimensions']['path'] = os.path.join(*ppath.parts)
                return match

        # no match
        for dimension in dimensions:
            match['dimensions'][dimension] = None
        match['dimensions']['path'] = None
        return match

    def get_dimension_possibilities(self, fragment, path, **kwargs):
        dimension_possibilities = []
        for dimension in self.get_dimensions_list():
            possibilities = {'name': dimension}
            if dimension in kwargs:
                possibilities['options'] \
                    = self.get_dimension_inheritance(
                        dimension, kwargs[dimension])
            else:
                possibilities['options'] = ['all']
            dimension_possibilities.append(possibilities)
        paths = {'name': 'path', 'options': []}
        for subdir in self.split_path(path):
            paths['options'].append(os.path.join(subdir, fragment))
        dimension_possibilities.append(paths)

        return dimension_possibilities

    def get_fragment_paths(self, fragment, path, **kwargs):
        possibilities \
            = self.get_dimension_possibilities(fragment, path, **kwargs)

        # move the path (last possibility returned) to the start
        # so that it sorts correctly when coming out of itertools.product
        possibilities.insert(0, possibilities.pop())

        paths = []
        options = [ poss['options'] for poss in possibilities ]
        for combo in itertools.product(*options):
            # if all non-path dimensions are "all", that is equivalent
            # to "default" so skip the combo
            if combo[1:].count('all') != len(combo[1:]):
                # put the path back on the end, reversing what we did
                # above so that it would compute the product correctly
                paths.append(os.path.join(*combo[1:], combo[0]))

        # 'default' ("all/all/all...") special cases
        for path in options[0]:
            paths.append(os.path.join('default', path))
        return paths

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

    def get_fragment_file(self, file):
        path = os.path.join(self.fragments_directory, file)
        with open(path) as handle:
            return handle.read()

    def build_dimensions(self, dimensions):
        if not dimensions:
            try:
                dimensions = toml.load(
                    os.path.join(self.fragments_directory, 'dimensions.toml')
                )
            except FileNotFoundError:
                dimensions = {}
        for dimension in RESERVED_DIMENSIONS:
            if dimension in dimensions:
                raise KeyError(
                    '"%s" is a reserved dimension name' % dimension
                )
        for dimension in dimensions:
            for instance in dimensions[dimension]:
                if instance in RESERVED_DIMENSION_INSTANCES:
                    raise KeyError(
                        '"%s" is a reserved dimension instance name'
                        % dimension
                    )
        return dimensions

    def build_targets(self, targets):
        if not targets:
            try:
                targets = toml.load(
                    os.path.join(self.fragments_directory, 'targets.toml')
                )
            except FileNotFoundError:
                targets = []
        return targets
