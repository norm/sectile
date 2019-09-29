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
            [{ 'something': 'default/something', 'depth': 1}]
        )
    )

    assert (
        sectile.expand('\n[[ sectile insert nothing ]]\n', '')
        == (
            '\n\n',
            [{ 'nothing': None, 'depth': 1}]
        )
    )

def test_expand_line_alone_has_no_duplicate_newline():
    sectile = Sectile(fragments='tests/fragments')
    assert (
        sectile.expand('before\n[[ sectile insert title ]]\nafter', '')
        == (
            'before\n<title>default page title</title>\nafter',
            [{ 'title': 'default/title', 'depth': 1}]
        )
    )

def test_expand_inline_has_no_newline():
    sectile = Sectile(fragments='tests/fragments')
    assert (
        sectile.expand('before [[ sectile insert title ]] after', '')
        == (
            'before <title>default page title</title> after',
            [{ 'title': 'default/title', 'depth': 1}]
        )
    )
