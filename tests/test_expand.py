import pytest

from sectile import Sectile


def test_expand_raises_error_without_arguments():
    with pytest.raises(TypeError):
        sectile = Sectile(fragments='tests/fragments')
        sectile.expand()


def test_expand_raises_error_on_nonstring():
    with pytest.raises(TypeError):
        sectile = Sectile(fragments='tests/fragments')
        sectile.expand(1234)


def test_expand_returns_strings_unchanged():
    sectile = Sectile(fragments='tests/fragments')
    assert sectile.expand('', '') == ('', [])
    assert sectile.expand('a string', '') == ('a string', [])
    assert sectile.expand('\nhello\n', '') == ('\nhello\n', [])
    assert sectile.expand('1234', '') == ('1234', [])


def test_expand_expands():
    sectile = Sectile(fragments='tests/fragments')
    assert (
        sectile.expand('\n[[ sectile insert something ]]\n', '')
        == (
            '\nFOUND SOMETHING\n',
            [{
                'dimensions': {
                    'region': 'all',
                    'product': 'all',
                    'environment': 'all',
                    'path': 'something',
                },
                'file': 'something',
                'found': 'default/something',
                'fragment': 'FOUND SOMETHING',
                'depth': 1,
            }]
        )
    )

    assert (
        sectile.expand('\n[[ sectile insert nothing ]]\n', '')
        == (
            '\n\n',
            [{
                'dimensions': {
                    'environment': None,
                    'product': None,
                    'region': None,
                    'path': None,
                },
                'file': 'nothing',
                'found': None,
                'fragment': '',
                'depth': 1,
            }]
        )
    )

def test_expand_line_alone_has_no_duplicate_newline():
    sectile = Sectile(fragments='tests/fragments')
    assert (
        sectile.expand('before\n[[ sectile insert title ]]\nafter', '')
        == (
            'before\n<title>default page title</title>\nafter',
            [{
                'dimensions': {
                    'region': 'all',
                    'product': 'all',
                    'environment': 'all',
                    'path': 'title',
                },
                'file': 'title',
                'found': 'default/title',
                'fragment': '<title>default page title</title>\n',
                'depth': 1,
            }]
        )
    )

def test_expand_inline_has_no_newline():
    sectile = Sectile(fragments='tests/fragments')
    assert (
        sectile.expand('before [[ sectile insert title ]] after', '')
        == (
            'before <title>default page title</title> after',
            [{
                'dimensions': {
                    'region': 'all',
                    'product': 'all',
                    'environment': 'all',
                    'path': 'title',
                },
                'file': 'title',
                'found': 'default/title',
                'fragment': '<title>default page title</title>\n',
                'depth': 1,
            }]
        )
    )
