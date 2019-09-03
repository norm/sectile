import pytest
import toml

from sectile import Sectile


def test_read_dimensions_file():
    sectile = Sectile('tests/fragments')
    assert sectile.get_dimensions_list() == [
        'region',
        'language',
        'environment',
    ]

    assert sectile.get_dimension('region') == {'england': 'uk', 'uk': 'europe'}
    assert sectile.get_dimension('language') == {}
    assert sectile.get_dimension('environment') == {'qa': 'staging', 'staging': 'production'}


def test_read_broken_dimensions_file():
    """ A broken TOML file means we stop immediately. """
    with pytest.raises(toml.TomlDecodeError):
        sectile = Sectile('tests/broken_fragments')
        sectile.get_dimensions_list()


def test_read_missing_dimensions_file():
    """ A missing dimensions.toml file is acceptable """
    sectile = Sectile('tests/missing_fragments')
    assert sectile.get_dimensions_list() == []


def test_add_missing_dimensions_to_empty_file():
    """ An empty dimensions.toml file is acceptable """
    sectile = Sectile('tests/empty_fragments')
    assert sectile.get_dimensions_list() == []


def test_dimension_inheritance_across_keys():
    sectile = Sectile('tests/fragments')
    assert (
        sectile.get_dimension_inheritance('region', 'england')
        == ['england', 'uk', 'europe', 'all']
    )

def test_dimension_inheritance_doesnt_require_entry_in_config():
    sectile = Sectile('tests/fragments')
    assert (
        sectile.get_dimension_inheritance('region', 'latvia')
        == ['latvia', 'all']
    )
