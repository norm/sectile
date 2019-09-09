What is sectile?
================

Sectile is a file generator, or pre-processor. It is used to create more
complex files used in other software from many small fragments. It is best
used where multiple files are quite similar, and share a common structure, but
have differences that need to be addressed.

An illustrative example is HTML templates in web applications: the basic
structure of the template is the same (doctype, head section, global
navigation, footers, etc.) but each section/type of page could have unique
differences even while sharing common areas, modules, or themes.


Example
-------

To show what sectile looks like in action, let us use the HTML example. A
basic HTML page:

    <!DOCTYPE html>
    <head>
      <meta charset="utf-8">
      <link rel="stylesheet" href="/css/site.css">
      <title>A page</title>
    </head>
    <body>
      <h1>This is a page</h1>
    </body>
    </html>

But while you are unlikely to vary from using UTF-8 on pages, and a site-wide
CSS file is common, few pages would have the same title or the same body.
Breaking these sections out looks like:

    <!DOCTYPE html>
    <head>
      <meta charset="utf-8">
      <link rel="stylesheet" href="/css/site.css">
      [[ sectile insert head_title ]]
    </head>
    <body>
      [[ sectile insert body_content ]]
    </body>
    </html>

When you generate a page or section's template using sectile, it will look
through a directory structure to find the two files called `head_title` and
`body_content`, and insert them.

The real power of sectile, however, comes from how it looks for fragments when
putting a file together. When you generate content using sectile, you declare
the destination path of the content (for example, the URL of the web page, or
the template file you are about to write out) and any optional
[dimensions](/dimensions/) which represent extra context about the
destination.

### Destination paths

When looking for `head_title` when generating to a destination path of
`blog/article/some-article`, sectile would look for this in a most-specific to
least-specific order:

    * `default/blog/article/some-article/head_title`
    * `default/blog/article/head_title`
    * `default/blog/head_title`
    * `default/head_title`

**Note:** The first part of the path to possible fragments (`default/`) is
used by sectile to represent an absence of dimensions, which are explained
next.

By creating a fragment at a more specific level, you are making content that
is more localised to exactly the content you are generating. By creating a
fragment at a less specific level, you are making content that is useful 
across a wider variety of destinations.

### Dimensions

Sometimes you could be creating content that uses the same destination path,
but is different in some other way. You might be creating multiple versions
of a website that represents the same content but in different languages. Or
multiple versions that have identical content apart from some third-party
logo, when [white-labelling](https://en.wikipedia.org/wiki/White-label_product)
content. Sectile represents this with dimensions. You can define as many
dimensions as you need to differentiate versions of your content, and then
create instances within those dimensions to represent the versions themselves.

Instances within dimensions have inheritance from other dimensions, so they
too can be treated as most-specific to least-specific. A generic base level of
inheritance always exists, so there will always be at least two possibilities
for every dimension you are using.

For example, if a dimension that represents language was being used, it could
be set up to represent specific dialects but still use the more generic
language if there was no specific content for a dialect, such as for the
Québécois (Quebec French) dialect:

    * `quebec-french/head_title`
    * `canadian-french/head_title`
    * `french/head_title`
    * `default/head_title`

**Note:** The last option (`default`) is used by sectile to represent the base
level of inheritance, rather than ending with `/head_title`.

### How paths and dimensions combine

When generating content that has both a specific path and multiple dimensions,
sectile can end up looking in many possible locations to find the desired
fragment.

Sectile combines the dimensions (in the order they have been declared) and the
path, and tries to find a fragment. It will then step back through the
dimensions and path to try less specific versions until it gets to the default
content.

Using an example path of `blog/article` and two dimensions, `language`
set to `english`, and `environment` set to `production`, sectile would try
the following twelve locations in order to locate a `head_title` fragment:

    * 'english/production/blog/article/head_title'
    * 'english/all/blog/article/head_title'
    * 'all/production/blog/article/head_title'
    * 'english/production/blog/head_title'
    * 'english/all/blog/head_title'
    * 'all/production/blog/head_title'
    * 'english/production/head_title'
    * 'english/all/head_title'
    * 'all/production/head_title'
    * 'default/blog/article/head_title'
    * 'default/blog/head_title'
    * 'default/head_title'

There are twelve possibilities as it is the product of combining each of
three possibilities for path, two for the `language` domain, and two for the
`environment` domain.

Let's step through them in more detail.

The first three attempts all try to find the fragment using the most specific
path (`blog/article`) within the declared dimensions. As `language` was
defined before `environment` it is considered more important, so the less
specific default instance (represented as `all`) for `environment` is tried in
combination with `english` for `language` before the combination of `all` for
`language` and `production` for `environment`.

    * 'english/production/blog/article/head_title'
    * 'english/all/blog/article/head_title'
    * 'all/production/blog/article/head_title'

Then these three dimension combinations are tried again for the less specific
`blog` part of the path:

    * 'english/production/blog/head_title'
    * 'english/all/blog/head_title'
    * 'all/production/blog/head_title'

Then again without any path:

    * 'english/production/head_title'
    * 'english/all/head_title'
    * 'all/production/head_title'

Then lastly, the base level of inheritance is checked once for each part of
the path. Note this is the same as using only a path without dimensions as
illustrated earlier.

    * 'default/blog/article/head_title'
    * 'default/blog/head_title'
    * 'default/head_title'

You can think of the final options under `default/` as representing the
combination of the base (`all`) instance for every domain being combined
with each possibility for the path.
