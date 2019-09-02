import pytest

from sectile import Sectile


def test_expand_raises_error_without_arguments():
    with pytest.raises(TypeError):
        sectile = Sectile('tests/fragments')
        sectile.expand()


def test_expand_raises_error_on_nonstring():
    with pytest.raises(TypeError):
        sectile = Sectile('tests/fragments')
        sectile.expand(1234)


def test_expand_returns_strings_unchanged():
    sectile = Sectile('tests/fragments')
    assert sectile.expand('') == ''
    assert sectile.expand('a string') == 'a string'
    assert sectile.expand('\nhello\n') == '\nhello\n'
    assert sectile.expand('1234') == '1234'


def test_expand_expands():
    sectile = Sectile('tests/fragments')
    assert (
        sectile.expand('\n[[ sectile insert something ]]\n', '')
        == '\nFOUND SOMETHING\n'
    )
