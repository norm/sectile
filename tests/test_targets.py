import os
from shutil import rmtree
from tempfile import mkdtemp

from sectile import Sectile


class CompareDirectories:
    def setup_method(self, meth):
        self.tempdir = mkdtemp()

    def teardown_method(self, meth):
        rmtree(self.tempdir)

    def compare_directories(self):
        tested_files = self.relative_list_of_files_in_directory(self.tempdir)
        assert sorted(self.expected_files) == sorted(tested_files)

        for filename in self.expected_files:
            self.compare_file(filename)

    def compare_file(self, filename):
        expected_file = '%s/%s' % (self.expected_directory, filename)
        tested_file = '%s/%s' % (self.tempdir, filename)
        with open(expected_file) as file:
            expected = file.read()
        with open(tested_file) as file:
            tested = file.read()

        assert expected == tested

    def relative_list_of_files_in_directory(self, directory):
        _file_list = []
        _trim = len(directory) + 1
        for _root, _dirs, _files in os.walk(directory):
            _subdir = _root[_trim:]
            for _file in _files:
                if len(_subdir):
                    _file_list.append('%s/%s' % (_subdir, _file))
                else:
                    _file_list.append(_file)
        return _file_list


class TestSectileTargetGeneration(CompareDirectories):
    expected_directory = 'tests/generated'
    expected_files = [
        'england/all/staging/index.html',
        'england/all/staging/about.html',
        'england/all/all/index.html',
        'england/all/all/about.html',
        'england/all/qa/index.html',
        'england/all/qa/about.html',
        'england/all/production/index.html',
        'england/all/production/about.html',
        'us/all/staging/index.html',
        'us/all/staging/about.html',
        'us/all/all/index.html',
        'us/all/all/about.html',
        'us/all/qa/index.html',
        'us/all/qa/about.html',
        'us/all/production/index.html',
        'us/all/production/about.html',
    ]

    def test_target_generation(self):
        sectile = Sectile(
            'tests/fragments',
            self.tempdir,
        )
        sectile.generate_all_targets()
        self.compare_directories()
