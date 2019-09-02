from sectile import Sectile


def test_read_dimensions_file():
    sectile = Sectile('tests/fragments')
    assert sectile.get_dimensions() == (
    )