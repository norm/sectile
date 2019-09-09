from sectile import Sectile


def test_fragment_alone():
    sectile = Sectile('tests/empty_fragments')
    assert (
        sectile.get_fragment_paths('header', '')
        == [
            'default/header',
        ]
    )

def test_with_path_but_no_dimensions():
    sectile = Sectile('tests/empty_fragments')
    assert (
        sectile.get_fragment_paths(
            'header',
            'blog/section/article'
        ) == [
            'default/blog/section/article/header',
            'default/blog/section/header',
            'default/blog/header',
            'default/header',
        ]
    )
    assert (
        sectile.get_fragment_paths(
            'header',
            '///blog//../blog///article'
        ) == [
            'default/blog/article/header',
            'default/blog/header',
            'default/header',
        ]
    )


def test_fragment_paths():
    sectile = Sectile('tests/fragments')
    assert (
        sectile.get_fragment_paths(
            'header',
            'blog/article',
            region='england',
            environment='qa',
        ) == [
            'england/all/qa/blog/article/header',
            'england/all/staging/blog/article/header',
            'england/all/production/blog/article/header',
            'england/all/all/blog/article/header',
            'uk/all/qa/blog/article/header',
            'uk/all/staging/blog/article/header',
            'uk/all/production/blog/article/header',
            'uk/all/all/blog/article/header',
            'europe/all/qa/blog/article/header',
            'europe/all/staging/blog/article/header',
            'europe/all/production/blog/article/header',
            'europe/all/all/blog/article/header',
            'all/all/qa/blog/article/header',
            'all/all/staging/blog/article/header',
            'all/all/production/blog/article/header',
            'england/all/qa/blog/header',
            'england/all/staging/blog/header',
            'england/all/production/blog/header',
            'england/all/all/blog/header',
            'uk/all/qa/blog/header',
            'uk/all/staging/blog/header',
            'uk/all/production/blog/header',
            'uk/all/all/blog/header',
            'europe/all/qa/blog/header',
            'europe/all/staging/blog/header',
            'europe/all/production/blog/header',
            'europe/all/all/blog/header',
            'all/all/qa/blog/header',
            'all/all/staging/blog/header',
            'all/all/production/blog/header',
            'england/all/qa/header',
            'england/all/staging/header',
            'england/all/production/header',
            'england/all/all/header',
            'uk/all/qa/header',
            'uk/all/staging/header',
            'uk/all/production/header',
            'uk/all/all/header',
            'europe/all/qa/header',
            'europe/all/staging/header',
            'europe/all/production/header',
            'europe/all/all/header',
            'all/all/qa/header',
            'all/all/staging/header',
            'all/all/production/header',
            'default/blog/article/header',
            'default/blog/header',
            'default/header',
        ]
    )


def test_find_fragments():
    sectile = Sectile('tests/fragments')
    assert (
        sectile.get_fragment(
            'header',
            '',
            region='england',
        ) == 'european header\n'
    )
    assert (
        sectile.get_fragment(
            'header',
            '',
            region='england',
            environment='qa',
        ) == 'UK QA header\n'
    )
    assert (
        sectile.get_fragment(
            'header',
            'blog/article',
            region='england',
        ) == 'England blog header\n'
    )
    assert (
        sectile.get_fragment(
            'blog/article/snarf',
            '',
            region='england',
        ) == None
    )