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

The real power of sectile, however, comes from how it looks for fragments
when putting a file together.
