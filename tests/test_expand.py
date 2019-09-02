import pytest

from sectile import Sectile


def test_expand_raises_error_without_arguments():
    with pytest.raises(TypeError):
        sectile = Sectile()
        sectile.expand()

def test_expand_returns_strings_unchanged():
    sectile = Sectile()
    assert sectile.expand('') == ''
    assert sectile.expand('a string') == 'a string'
    assert sectile.expand('\nhello\n') == '\nhello\n'
    assert sectile.expand(1234) == 1234
