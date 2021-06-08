import os
import pytest
from sectile import Sectile


def test_create_more_specific_fragment():
    sectile = Sectile(fragments='tests/fragments')
    target_fragment = 'tests/fragments/us/all/production/title'

    try:
        os.remove(target_fragment)
    except FileNotFoundError:
        pass
    assert not os.path.exists(target_fragment)

    sectile.create_fragment(
        'title',
        '',
        region='us',
        environment='production',
    )
    assert os.path.exists(target_fragment)

    match = sectile.get_matching_fragment(
            'title',
            '',
            region='us',
            environment='production',
        )
    assert match == {
            'dimensions': {
                'region': 'us',
                'product': 'all',
                'environment': 'production',
                'path': 'title',
            },
            'found': 'us/all/production/title',
        }
    assert sectile.get_fragment_file(match['found']) \
        == '<title>default page title</title>\n'

    # no error occurs (it is fine to "create" a fragment that already exists)
    with pytest.raises(FileExistsError):
        sectile.create_fragment(
            'title',
            '',
            region='us',
            environment='production',
        )

def test_create_default_fragment():
    sectile = Sectile(fragments='tests/fragments')
    target_fragment = 'tests/fragments/default/blog/created'
    incorrect_fragment = 'tests/fragments/all/all/all/blog/created'

    try:
        os.remove(target_fragment)
    except (FileNotFoundError, NotADirectoryError) as e:
        pass
    assert not os.path.exists(target_fragment)

    sectile.create_fragment(
        'created',
        'blog',
        region='all',
        product='all',
        environment='all',
    )
    assert not os.path.exists(incorrect_fragment)
    assert os.path.exists(target_fragment)

    match = sectile.get_matching_fragment(
            'created',
            'blog',
        )
    assert match == {
            'dimensions': {
                'region': 'all',
                'product': 'all',
                'environment': 'all',
                'path': 'blog/created',
            },
            'found': 'default/blog/created',
        }
    assert sectile.get_fragment_file(match['found']) == ''


def test_update_fragment():
    sectile = Sectile(fragments='tests/fragments')
    target_fragment = 'tests/fragments/us/all/production/title'

    try:
        os.remove(target_fragment)
    except FileNotFoundError:
        pass
    assert not os.path.exists(target_fragment)

    sectile.create_fragment(
        'title',
        '',
        region='us',
        environment='production',
    )
    assert os.path.exists(target_fragment)
    with open(target_fragment) as handle:
        assert handle.read() == '<title>default page title</title>\n'

    sectile.update_fragment('us/all/production/title', 'test content\n')

    with open(target_fragment) as handle:
        assert handle.read() == 'test content\n'


def test_delete_fragment():
    sectile = Sectile(fragments='tests/fragments')
    target_fragment = 'tests/fragments/us/all/production/title'

    if not os.path.exists(target_fragment):
        sectile.create_fragment(
            'title',
            '',
            region='us',
            environment='production',
        )
    assert os.path.exists(target_fragment)

    sectile.delete_fragment('us/all/production/title')
    assert not os.path.exists(target_fragment)

    with pytest.raises(FileNotFoundError):
        sectile.delete_fragment('us/all/production/title')
