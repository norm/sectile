import pytest

from sectile import Sectile


def test_generate_file_not_found():
    sectile = Sectile('tests/fragments')
    with pytest.raises(FileNotFoundError):
        assert sectile.generate('what/ever', 'no_such_template')


def test_generate_default_target():
    sectile = Sectile('tests/fragments')
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
        { 'default.html': 'default/default.html', 'depth': 0 },
        { 'head_wrapper': 'default/head_wrapper', 'depth': 1 },
        { 'title': 'default/title', 'depth': 2 },
        { 'body_wrapper': 'default/body_wrapper', 'depth': 1 },
        { 'body': 'default/body', 'depth': 2 },
    ]


def test_generate_specific_target():
    sectile = Sectile('tests/fragments')
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
        { 'default.html': 'default/default.html', 'depth': 0 },
        { 'head_wrapper': 'default/head_wrapper', 'depth': 1 },
        { 'title': 'europe/all/all/title', 'depth': 2 },
        { 'body_wrapper': 'default/body_wrapper', 'depth': 1 },
        { 'body': 'england/all/all/blog/body', 'depth': 2 },
    ]

def test_generate_with_missing_fragment():
    sectile = Sectile('tests/fragments')
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
        { 'default.html': 'default/default.html', 'depth': 0 },
        { 'head_wrapper': 'england/all/qa/head_wrapper', 'depth': 1 },
        { 'qa_css': None, 'depth': 2 },
        { 'title': 'europe/all/all/title', 'depth': 2 },
        { 'body_wrapper': 'default/body_wrapper', 'depth': 1 },
        { 'body': 'england/all/all/blog/body', 'depth': 2 },
    ]
