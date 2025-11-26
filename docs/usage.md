---
title: Usage
---

Command line arguments starting with `-` are interpreted as options,
everything else as filenames or URLs. All options except *flag* options
(or choice options which include `yes`) require a parameter in the form
`--option=value`.

One exception is the lone `-` (without anything else), which means media
data will be read from stdin. Also, `--` (without anything else) will
make the player interpret all following arguments as filenames, even if
they start with `-`. (To play a file named `-`, you need to use `./-`.)

Every *flag* option has a *no-flag* counterpart, e.g. the opposite of
the `--fs` option is `--no-fs`. `--fs=yes` is same as `--fs`, `--fs=no`
is the same as `--no-fs`.

If an option is marked as *(XXX only)*, it will only work in combination
with the *XXX* option or if *XXX* is compiled in.

#### Legacy option syntax

The `--option=value` syntax is not strictly enforced, and the
alternative legacy syntax `-option value` and `-option=value` will also
work. This is mostly for compatibility with MPlayer. Using these should
be avoided. Their semantics can change any time in the future.

For example, the alternative syntax will consider an argument following
the option a filename. `mpv -fs no` will attempt to play a file named
`no`, because `--fs` is a flag option that requires no parameter. If an
option changes and its parameter becomes optional, then a command line
using the alternative syntax will break.

Until mpv 0.31.0, there was no difference whether an option started with
`--` or a single `-`. Newer mpv releases strictly expect that you pass
the option value after a `=`. For example, before `mpv --log-file f.txt`
would write a log to `f.txt`, but now this command line fails, as
`--log-file` expects an option value, and `f.txt` is simply considered a
normal file to be played (as in `mpv f.txt`).

The future plan is that `-option value` will not work anymore, and
options with a single `-` behave the same as `--` options.

#### Escaping spaces and other special characters

Keep in mind that the shell will partially parse and mangle the
arguments you pass to mpv. For example, you might need to quote or
escape options and filenames:

> `mpv "filename with spaces.mkv" --title="window title"`

It gets more complicated if the suboption parser is involved. The
suboption parser puts several options into a single string, and passes
them to a component at once, instead of using multiple options on the
level of the command line.

The suboption parser can quote strings with `"` and `[...]`.
Additionally, there is a special form of quoting with `%n%` described
below.

For example, assume the hypothetical `foo` filter can take multiple
options:

> `mpv test.mkv --vf=foo:option1=value1:option2:option3=value3,bar`

This passes `option1` and `option3` to the `foo` filter, with `option2`
as flag (implicitly `option2=yes`), and adds a `bar` filter after that.
If an option contains spaces or characters like `,` or `:`, you need to
quote them:

> `mpv '--vf=foo:option1="option value with spaces",bar'`

Shells may actually strip some quotes from the string passed to the
commandline, so the example quotes the string twice, ensuring that mpv
receives the `"` quotes.

The `[...]` form of quotes wraps everything between `[` and `]`. It's
useful with shells that don't interpret these characters in the middle
of an argument (like bash). These quotes are balanced (since mpv 0.9.0):
the `[` and `]` nest, and the quote terminates on the last `]` that has
no matching `[` within the string. (For example, `[a[b]c]` results in
`a[b]c`.)

The fixed-length quoting syntax is intended for use with external
scripts and programs.

It is started with `%` and has the following format:

    %n%string_of_length_n

<div class="admonition" markdown="1">

Examples

`mpv '--vf=foo:option1=%11%quoted text' test.avi`

Or in a script:

`` mpv --vf=foo:option1=%`expr length "$NAME"`%"$NAME" test.avi ``

</div>

Note: where applicable with JSON-IPC, `%n%` is the length in UTF-8
bytes, after decoding the JSON data.

Suboptions passed to the client API are also subject to escaping. Using
`mpv_set_option_string()` is exactly like passing `--name=data` to the
command line (but without shell processing of the string). Some options
support passing values in a more structured way instead of flat strings,
and can avoid the suboption parsing mess. For example, `--vf` supports
`MPV_FORMAT_NODE`, which lets you pass suboptions as a nested data
structure of maps and arrays.

#### Paths

Some care must be taken when passing arbitrary paths and filenames to
mpv. For example, paths starting with `-` will be interpreted as
options. Likewise, if a path contains the sequence `://`, the string
before that might be interpreted as protocol prefix, even though `://`
can be part of a legal UNIX path. To avoid problems with arbitrary
paths, you should be sure that absolute paths passed to mpv start with
`/`, and prefix relative paths with `./`.

Using the `file://` pseudo-protocol is discouraged, because it involves
strange URL unescaping rules.

The name `-` itself is interpreted as stdin, and will cause mpv to
disable console controls. (Which makes it suitable for playing data
piped to stdin.)

The special argument `--` can be used to stop mpv from interpreting the
following arguments as options.

For paths passed to mpv suboptions (options that have multiple
<span class="title-ref">:</span> and
<span class="title-ref">,</span>-separated values), the situation is
further complicated by the need to escape special characters. To work
around this, the path can instead be wrapped in the "fixed-length"
syntax, e.g. `%n%string_of_length_n` (see above).

When using the libmpv API, you should strictly avoid using
`mpv_command_string` for invoking the `loadfile` command, and instead
prefer e.g. `mpv_command` to avoid the need for filename escaping.

The same applies when you're using the scripting API, where you should
avoid using `mp.command`, and instead prefer using "separate parameter"
APIs, such as `mp.commandv` and `mp.command_native`.

Some mpv options will interpret special meanings for paths starting with
`~`, making it easy to dynamically find special directories, such as
referring to the current user's home directory or the mpv configuration
directory.

When using the special `~` prefix, there must always be a trailing `/`
after the special path prefix. In other words, `~` doesn't work, but
`~/` will work.

The following special paths/keywords are currently recognized:

<div class="warning" markdown="1">

<div class="title" markdown="1">

Warning

</div>

Beware that if `--no-config` is used, all of the "config
directory"-based paths (`~~/`, `~~home/` and `~~global/`) will be empty
strings.

This means that `~~home/` would expand to an empty string, and that
sub-paths such as `~~home/foo/bar"` would expand to a relative path
(`foo/bar`), which may not be what you expected.

Furthermore, any commands that search in config directories will fail to
find anything, since there won't be any directories to search in.

Be sure that your scripts can handle these "no config" scenarios.

</div>

| Name | Meaning |
|----|----|
| `~/` | The current user's home directory (equivalent to `~/` and `$HOME/` in terminal environments). |
| `~~/` | If the sub-path exists in any of mpv's config directories, then the path of the existing file/dir is returned. Otherwise this is equivalent to `~~home/`. |
| `~~home/` | mpv's config dir (for example `~/.config/mpv/`). |
| `~~global/` | The global config path (such as `/etc/mpv`), if available (not on win32). |
| `~~osxbundle/` | The macOS bundle resource path (macOS only). |
| `~~desktop/` | The path to the desktop (win32, macOS). |
| `~~exe_dir/` | The path to the directory containing `mpv.exe` (for config file purposes, `$MPV_HOME` will override this) (win32 only). |
| `~~cache/` | The path to application cache data (`~/.cache/mpv/`). On some platforms, this will be the same as `~~home/`. |
| `~~state/` | The path to application state data (`~/.local/state/mpv/`). On some platforms, this will be the same as `~~home/`. |
| `~~old_home/` | Do not use. |

#### Per-File Options

When playing multiple files, any option given on the command line
usually affects all files. Example:

    mpv --a file1.mkv --b file2.mkv --c

| File      | Active options |
|-----------|----------------|
| file1.mkv | `--a --b --c`  |
| file2.mkv | `--a --b --c`  |

(This is different from MPlayer and mplayer2.)

Also, if any option is changed at runtime (via input commands), they are
not reset when a new file is played.

Sometimes, it is useful to change options per-file. This can be achieved
by adding the special per-file markers `--{` and `--}`. (Note that you
must escape these on some shells.) Example:

    mpv --a file1.mkv --b --\{ --c file2.mkv --d file3.mkv --e --\} file4.mkv --f

| File      | Active options            |
|-----------|---------------------------|
| file1.mkv | `--a --b --f`             |
| file2.mkv | `--a --b --f --c --d --e` |
| file3.mkv | `--a --b --f --c --d --e` |
| file4.mkv | `--a --b --f`             |

Additionally, any file-local option changed at runtime is reset when the
current file stops playing. If option `--c` is changed during playback
of `file2.mkv`, it is reset when advancing to `file3.mkv`. This only
affects file-local options. The option `--a` is never reset here.

#### List Options

Some options which store lists of option values can have action
suffixes. For example, the `--display-tags` option takes a `,`-separated
list of tags, but the option also allows you to append a single tag with
`--display-tags-append`, and the tag name can for example contain a
literal `,` without the need for escaping.

##### String list and path list options

String lists are separated by `,`. The strings are not parsed or
interpreted by the option system itself. However, most path or file list
options use `:` (Unix) or `;` (Windows) as separator, instead of `,`.

They support the following operations:

<table>
<thead>
<tr>
<th>Suffix</th>
<th>Meaning</th>
</tr>
</thead>
<tbody>
<tr>
<td><dl>
<dt><code>-set</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Set a list of items (using the list separator, escaped with
backslash)</td>
</tr>
<tr>
<td><dl>
<dt><code>-append</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append single item (does not interpret escapes)</td>
</tr>
<tr>
<td><dl>
<dt><code>-add</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append 1 or more items (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-pre</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Prepend 1 or more items (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-clr</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Clear the option (remove all items)</td>
</tr>
<tr>
<td><dl>
<dt><code>-del</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Delete 1 or more items if present (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-remove</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Delete item if present (does not interpret escapes)</td>
</tr>
<tr>
<td><dl>
<dt><code>-toggle</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append an item, or remove it if it already exists (no escapes)</td>
</tr>
</tbody>
</table>

`-append` is meant as a simple way to append a single item without
having to escape the argument (you may still need to escape on the shell
level).

##### Key/value list options

A key/value list is a list of key/value string pairs. In programming
languages, this type of data structure is often called a map or a
dictionary. The order normally does not matter, although in some cases
the order might matter.

They support the following operations:

<table>
<thead>
<tr>
<th>Suffix</th>
<th>Meaning</th>
</tr>
</thead>
<tbody>
<tr>
<td><dl>
<dt><code>-set</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Set a list of items (using <code>,</code> as separator)</td>
</tr>
<tr>
<td><dl>
<dt><code>-append</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append a single item (escapes for the key, no escapes for the
value)</td>
</tr>
<tr>
<td><dl>
<dt><code>-add</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append 1 or more items (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-clr</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Clear the option (remove all items)</td>
</tr>
<tr>
<td><dl>
<dt><code>-del</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Delete 1 or more keys if present (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-remove</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Delete item by key if present (does not interpret escapes)</td>
</tr>
</tbody>
</table>

Keys are unique within the list. If an already present key is set, the
existing key is removed before the new value is appended.

If you want to pass a value without interpreting it for escapes or `,`,
it is recommended to use the `-append` variant. When using libmpv,
prefer using `MPV_FORMAT_NODE_MAP`; when using a scripting backend or
the JSON IPC, use an appropriate structured data type.

Prior to mpv 0.33, `:` was also recognized as separator by `-set`.

##### Object settings list options

This is a very complex option type for some options, such as `--af` and
`--vf`. They often require complicated escaping. See [VIDEO
FILTERS](video-filters.md) for details.

They support the following operations:

<table>
<thead>
<tr>
<th>Suffix</th>
<th>Meaning</th>
</tr>
</thead>
<tbody>
<tr>
<td><dl>
<dt><code>-set</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Set a list of items (using <code>,</code> as separator)</td>
</tr>
<tr>
<td><dl>
<dt><code>-append</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append single item</td>
</tr>
<tr>
<td><dl>
<dt><code>-add</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append 1 or more items (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-pre</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Prepend 1 or more items (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-clr</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Clear the option (remove all items)</td>
</tr>
<tr>
<td><dl>
<dt><code>-remove</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Delete 1 or items if present (same syntax as -set)</td>
</tr>
<tr>
<td><dl>
<dt><code>-toggle</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Append an item, or remove it if it already exists</td>
</tr>
<tr>
<td><dl>
<dt><code>-help</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td>Pseudo operation that prints a help text to the terminal</td>
</tr>
</tbody>
</table>

##### General

Without suffix, the operation used is normally `-set`.

Some operations like `-add` and `-pre` specify multiple items, but be
aware that you may need to escape the arguments. `-append` accepts a
single, unescaped item only (so the `,` separator will not be
interpreted and is passed on as part of the value).

Some options (like `--sub-file`, `--audio-file`, `--glsl-shader`) are
aliases for the proper option with `-append` action. For example,
`--sub-file` is an alias for `--sub-files-append`.

Options of this type can be changed at runtime using the `change-list`
command, which takes the suffix (without the `-`) as separate operation
parameter.

An object settings list can hold up to 100 elements.

