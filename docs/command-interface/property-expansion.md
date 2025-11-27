---
title: Property Expansion
---

All string arguments to input commands as well as certain options (like
`--term-playing-msg`) are subject to property expansion. Note that
property expansion does not work in places where e.g. numeric parameters
are expected. (For example, the `add` command does not do property
expansion. The `set` command is an exception and not a general rule.)

<div class="admonition" markdown="1">

Example for input.conf

`i show-text "Filename: ${filename}"`

:   shows the filename of the current file when pressing the `i` key

</div>

Whether property expansion is enabled by default depends on which API is
used (see [Flat command syntax](flat-command-syntax.md), [Commands
specified as arrays](commands-specified-as-arrays.md) and [Named
arguments](named-arguments.md)), but it can always be enabled with the
`expand-properties` prefix or disabled with the `raw` prefix, as
described in [Input Command Prefixes](input-command-prefixes.md).

The following expansions are supported:

`${NAME}`

:   Expands to the value of the property `NAME`. If retrieving the
    property fails, expand to an error string. (Use `${NAME:}` with a
    trailing `:` to expand to an empty string instead.) If `NAME` is
    prefixed with `=`, expand to the raw value of the property (see
    section below).

`${NAME:STR}`

:   Expands to the value of the property `NAME`, or `STR` if the
    property cannot be retrieved. `STR` is expanded recursively.

`${?NAME:STR}`

:   Expands to `STR` (recursively) if the property `NAME` is available.

`${!NAME:STR}`

:   Expands to `STR` (recursively) if the property `NAME` cannot be
    retrieved.

`${?NAME==VALUE:STR}`

:   Expands to `STR` (recursively) if the property `NAME` expands to a
    string equal to `VALUE`. You can prefix `NAME` with `=` in order to
    compare the raw value of a property (see section below). If the
    property is unavailable, or other errors happen when retrieving it,
    the value is never considered equal. Note that `VALUE` can't contain
    any of the characters `:` or `}`. Also, it is possible that escaping
    with `"` or `%` might be added in the future, should the need arise.

`${!NAME==VALUE:STR}`

:   Same as with the `?` variant, but `STR` is expanded if the value is
    not equal. (Using the same semantics as with `?`.)

`$$`

:   Expands to `$`.

`$}`

:   Expands to `}`. (To produce this character inside recursive
    expansion.)

`$>`

:   Disable property expansion and special handling of `$` for the rest
    of the string.

In places where property expansion is allowed, C-style escapes are often
accepted as well. Example:

> - `\n` becomes a newline character
> - `\\` expands to `\`

