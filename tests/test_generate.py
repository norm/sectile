import pytest

from sectile import Sectile


# FIXME whitespace after includes

def test_generate_file_not_found():
    sectile = Sectile('tests/fragments')
    with pytest.raises(FileNotFoundError):
        assert sectile.generate_target('what/ever', 'no_such_template')


def test_generate_default_target():
    sectile = Sectile('tests/fragments')
    assert sectile.generate_target(
        'homepage',
        'default.html',
    ) == """<!DOCTYPE html>
<html>
<head>
</head>

<body>
<h1>This page type not defined</h1>

</body>

</html>
"""


def test_generate_specific_target():
    sectile = Sectile('tests/fragments')
    assert sectile.generate_target(
        'blog/article/13-things-to-do-in-london',
        'default.html',
        region='england',
        environment='production',
    ) == """<!DOCTYPE html>
<html>
<head>
</head>

<body>
<h1>An English blog page</h1>

</body>

</html>
"""
