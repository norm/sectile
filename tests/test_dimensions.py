import pytest
import toml

from sectile import Sectile


def test_dimensions_at_instantiation():
    sectile = Sectile(
        fragments = 'tests/empty_fragments',
        dimensions = {
            'region': {'england': 'uk'},
            'environment': {'staging': 'production'}
        }
    )
    assert sectile.get_dimensions_list() == [
        'region',
        'environment',
    ]
    assert sectile.get_dimension('region') == {'england': 'uk'}
    assert sectile.get_dimension('environment') == {'staging': 'production'}


def test_read_dimensions_file():
    sectile = Sectile(fragments='tests/fragments')
    assert sectile.get_dimensions_list() == [
        'region',
        'product',
        'environment',
    ]

    assert sectile.get_dimension('region') == {
        'england': 'uk',
        'uk': 'europe',
        'us': 'all',
    }
    assert sectile.get_dimension('product') == {}
    assert sectile.get_dimension('environment') == {
        'qa': 'staging',
        'staging': 'production',
    }


def test_dimensions_at_instantiation_overrides_toml():
    sectile = Sectile(
        fragments = 'tests/fragments',
        dimensions = {
            'region': {'england': 'uk'},
            'environment': {'staging': 'production'}
        }
    )
    assert sectile.get_dimensions_list() == [
        'region',
        'environment',
    ]
    assert sectile.get_dimension('region') == {'england': 'uk'}
    assert sectile.get_dimension('environment') == {'staging': 'production'}


def test_read_broken_dimensions_file():
    """ A broken TOML file means we stop immediately. """
    with pytest.raises(toml.TomlDecodeError):
        sectile = Sectile(fragments='tests/broken_fragments')
        sectile.get_dimensions_list()


def test_read_missing_dimensions_file():
    """ A missing dimensions.toml file is acceptable """
    sectile = Sectile(fragments='tests/missing_fragments')
    assert sectile.get_dimensions_list() == []


def test_add_missing_dimensions_to_empty_file():
    """ An empty dimensions.toml file is acceptable """
    sectile = Sectile(fragments='tests/empty_fragments')
    assert sectile.get_dimensions_list() == []


def test_dimension_inheritance_across_keys():
    sectile = Sectile(fragments='tests/fragments')
    assert (
        sectile.get_dimension_inheritance('region', 'england')
        == ['england', 'uk', 'europe', 'all']
    )

def test_dimension_inheritance_doesnt_require_entry_in_config():
    sectile = Sectile(fragments='tests/fragments')
    assert (
        sectile.get_dimension_inheritance('region', 'latvia')
        == ['latvia', 'all']
    )

def test_reserved_dimensions_cause_error():
    with pytest.raises(KeyError):
        sectile = Sectile(
            fragments = 'tests/empty_fragments',
            dimensions = {
                'dimension': { 'true': 'false' },
                'intl': { 'en-GB': 'en' },
            }
        )

def test_reserved_dimension_instances_cause_error():
    with pytest.raises(KeyError):
        sectile = Sectile(
            fragments = 'tests/empty_fragments',
            dimensions = {
                'product': { 'toaster': 'generic', 'generic': 'all' },
            }
        )
