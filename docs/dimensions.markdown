Using dimensions with sectile
=============================

Sectile can use dimensions to be able to vary what fragment is included when
generating content.


dimensions.toml
---------------

The dimensions are declared in the file `dimensions.toml` in the root of
your sectile directory.

    # dimensions.toml
    dimensions = [
        'region',
        'language',
        'environment',
    ]

    [region]
    # region instances go here

    [language]
    [environment]

Dimensions contain instances which represent a more specific type of fragment
than the default, which is named `all`:

    [region]
    "europe" = "all"

A fragment created for all regions would be used when generating content for
the `europe` region, unless there was a more specific file just for use in
the `europe` region.

Dimension instances can inherit from other instances:

    [region]
    "europe" = "all"
    "uk" = "europe"

When generating content for the `uk` region, it would check for fragments
specific to the `uk`, then to `europe`, then for `all` (and finally the 
default content which is not specific to dimensions at all).

**Note:** You do not have to declare a dimension instance that inherits
only from `all`, this is implied if there is no explicit inheritance declared.
The above example only needed to be

    [region]
    "uk" = "europe"


### Empty or missing dimensions.toml

Your sectile directory does not have to contain a dimensions file if you
do not wish to use dimensions.
