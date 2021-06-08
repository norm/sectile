import pytest

from sectile import Sectile


def test_generate_file_not_found():
    sectile = Sectile(fragments='tests/fragments')
    with pytest.raises(FileNotFoundError):
        assert sectile.generate('what/ever', 'no_such_template')


def test_generate_default_target():
    sectile = Sectile(fragments='tests/fragments')
    (content, fragments) = sectile.generate(
        'homepage',
        'default.html',
    )
    assert content == """<!DOCTYPE html>
<html>
<head>
<title>default page title</title>
</head>
<body>
<h1>This page type not defined</h1>
</body>
</html>
"""
    assert fragments == [
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'default.html',
            },
            'file': 'default.html',
            'found': 'default/default.html',
            'fragment': (
                '<!DOCTYPE html>\n'
                '<html>\n'
                '[[ sectile insert head_wrapper ]]\n'
                '[[ sectile insert body_wrapper ]]\n'
                '</html>\n'
            ),
            'depth': 0,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'head_wrapper',
            },
            'file': 'head_wrapper',
            'found': 'default/head_wrapper',
            'fragment': (
                '<head>\n'
                '[[ sectile insert title ]]\n'
                '</head>\n'
            ),
            'depth': 1,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'title',
            },
            'file': 'title',
            'found': 'default/title',
            'fragment': '<title>default page title</title>\n',
            'depth': 2,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'body_wrapper',
            },
            'file': 'body_wrapper',
            'found': 'default/body_wrapper',
            'fragment': (
                '<body>\n'
                '[[ sectile insert body ]]\n'
                '</body>\n'
            ),
            'depth': 1,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'body',
            },
            'file': 'body',
            'found': 'default/body',
            'fragment': '<h1>This page type not defined</h1>\n',
            'depth': 2,
        },
    ]


def test_generate_specific_target():
    sectile = Sectile(fragments='tests/fragments')
    (content, fragments) = sectile.generate(
        'blog/article/13-things-to-do-in-london',
        'default.html',
        region='england',
        environment='production',
    )

    assert content == """<!DOCTYPE html>
<html>
<head>
<title>European title</title>
</head>
<body>
<h1>An English blog page</h1>
</body>
</html>
"""
    assert fragments == [
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'default.html',
            },
            'file': 'default.html',
            'found': 'default/default.html',
            'fragment': (
                '<!DOCTYPE html>\n'
                '<html>\n'
                '[[ sectile insert head_wrapper ]]\n'
                '[[ sectile insert body_wrapper ]]\n'
                '</html>\n'
            ),
            'depth': 0,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'head_wrapper',
            },
            'file': 'head_wrapper',
            'found': 'default/head_wrapper',
            'fragment': (
                '<head>\n'
                '[[ sectile insert title ]]\n'
                '</head>\n'
            ),
            'depth': 1,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'europe',
                'path': 'title',
            },
            'file': 'title',
            'found': 'europe/all/all/title',
            'fragment': '<title>European title</title>',
            'depth': 2,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'body_wrapper',
            },
            'file': 'body_wrapper',
            'found': 'default/body_wrapper',
            'fragment': (
                '<body>\n'
                '[[ sectile insert body ]]\n'
                '</body>\n'
            ),
            'depth': 1,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'england',
                'path': 'blog/body',
            },
            'file': 'body',
            'found': 'england/all/all/blog/body',
            'fragment': '<h1>An English blog page</h1>\n',
            'depth': 2,
        },
    ]

def test_generate_with_missing_fragment():
    sectile = Sectile(fragments='tests/fragments')
    (content, fragments) = sectile.generate(
        'blog/article/13-things-to-do-in-london',
        'default.html',
        region='england',
        environment='qa',
    )

    assert content == """<!DOCTYPE html>
<html>
<head>

<title>European title</title>
</head>
<body>
<h1>An English blog page</h1>
</body>
</html>
"""
    assert fragments == [
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'default.html',
            },
            'file': 'default.html',
            'found': 'default/default.html',
            'fragment': (
                '<!DOCTYPE html>\n'
                '<html>\n'
                '[[ sectile insert head_wrapper ]]\n'
                '[[ sectile insert body_wrapper ]]\n'
                '</html>\n'
            ),
            'depth': 0,
        },
        {
            'dimensions': {
                'environment': 'qa',
                'product': 'all',
                'region': 'england',
                'path': 'head_wrapper',
            },
            'file': 'head_wrapper',
            'found': 'england/all/qa/head_wrapper',
            'fragment': (
                '<head>\n'
                '[[ sectile insert qa_css ]]\n'
                '[[ sectile insert title ]]\n'
                '</head>\n'
            ),
            'depth': 1,
        },
        {
            'dimensions': {
                'environment': None,
                'product': None,
                'region': None,
                'path': None,
            },
            'file': 'qa_css',
            'found': None,
            'fragment': '',
            'depth': 2,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'europe',
                'path': 'title',
            },
            'file': 'title',
            'found': 'europe/all/all/title',
            'fragment': '<title>European title</title>',
            'depth': 2,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'all',
                'path': 'body_wrapper',
            },
            'file': 'body_wrapper',
            'found': 'default/body_wrapper',
            'fragment': (
                '<body>\n'
                '[[ sectile insert body ]]\n'
                '</body>\n'
            ),
            'depth': 1,
        },
        {
            'dimensions': {
                'environment': 'all',
                'product': 'all',
                'region': 'england',
                'path': 'blog/body',
            },
            'file': 'body',
            'found': 'england/all/all/blog/body',
            'fragment': '<h1>An English blog page</h1>\n',
            'depth': 2,
        },
    ]
