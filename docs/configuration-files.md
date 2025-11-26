---
title: Configuration Files
---

#### Location and Syntax

You can put all of the options in configuration files which will be read
every time mpv is run. The system-wide configuration file 'mpv.conf' is
in your configuration directory (e.g. `/etc/mpv` or
`/usr/local/etc/mpv`), the user-specific one is
`~/.config/mpv/mpv.conf`. For details and platform specifics (in
particular Windows paths) see the [FILES](files.md) section.

User-specific options override system-wide options and options given on
the command line override both. The syntax of the configuration files is
`option=value`. Everything after a *\#* is considered a comment. Options
that work without values can be enabled by setting them to *yes* and
disabled by setting them to *no*, and if the value is omitted, *yes* is
implied. Even suboptions can be specified in this way.

<div class="admonition" markdown="1">

Example configuration file

    # Don't allow new windows to be larger than the screen.
    autofit-larger=100%x100%
    # Enable hardware decoding if available, =yes is implied.
    hwdec
    # Spaces don't have to be escaped.
    osd-playing-msg=File: ${filename}

</div>

#### Escaping special characters

This is done like with command line options. A config entry can be
quoted with `"`, `'`, as well as with the fixed-length syntax (`%n%`)
mentioned before. This is like passing the exact contents of the quoted
string as a command line option. C-style escapes are currently
<span id="not">not</span>\_ interpreted on this level, although some
options do this manually (this is a mess and should probably be changed
at some point). The shell is not involved here, so option values only
need to be quoted to escape `#` anywhere in the value, `"`, `'` or `%`
at the beginning of the value, and leading and trailing whitespace.

#### Putting Command Line Options into the Configuration File

Almost all command line options can be put into the configuration file.
Here is a small guide:

| Option              | Configuration file entry |
|---------------------|--------------------------|
| `--flag`            | `flag`                   |
| `-opt val`          | `opt=val`                |
| `--opt=val`         | `opt=val`                |
| `-opt "has spaces"` | `opt=has spaces`         |

#### File-specific Configuration Files

You can also write file-specific configuration files. If you wish to
have a configuration file for a file called 'video.avi', create a file
named 'video.avi.conf' with the file-specific options in it and put it
in `~/.config/mpv/`. You can also put the configuration file in the same
directory as the file to be played. Both require you to set the
`--use-filedir-conf` option (either on the command line or in your
global config file). If a file-specific configuration file is found in
the same directory, no file-specific configuration is loaded from
`~/.config/mpv`. In addition, the `--use-filedir-conf` option enables
directory-specific configuration files. For this, mpv first tries to
load a mpv.conf from the same directory as the file played and then
tries to load any file-specific configuration.

#### Profiles

To ease working with different configurations, profiles can be defined
in the configuration files. A profile starts with its name in square
brackets, e.g. `[my-profile]`. All following options will be part of the
profile. A description (shown by `--profile=help`) can be defined with
the `profile-desc` option. To end the profile, start another one or use
the profile name `default` to continue with normal options.

You can list profiles with `--profile=help`, and show the contents of a
profile with `--show-profile=<name>` (replace `<name>` with the profile
name). You can apply profiles on start with the `--profile=<name>`
option, or at runtime with the `apply-profile <name>` command.

<div class="admonition" markdown="1">

Example mpv config file with profiles

    # normal top-level option
    fullscreen=yes

    # a profile that can be enabled with --profile=big-cache
    [big-cache]
    cache=yes
    demuxer-max-bytes=512MiB
    demuxer-readahead-secs=20

    [network]
    profile-desc="profile for content over network"
    force-window=immediate
    # you can also include other profiles
    profile=big-cache

    [reduce-judder]
    video-sync=display-resample
    interpolation=yes

    # using a profile again extends it
    [network]
    demuxer-max-back-bytes=512MiB
    # reference a builtin profile
    profile=fast

</div>

#### Runtime profiles

Profiles can be set at runtime with `apply-profile` command. Since this
operation is "destructive" (every item in a profile is simply set as an
option, overwriting the previous value), you can't just enable and
disable profiles again.

As a partial remedy, there is a way to make profiles save old option
values before overwriting them with the profile values, and then
restoring the old values at a later point using
`apply-profile <profile-name> restore`.

This can be enabled with the `profile-restore` option, which takes one
of the following options:

> 
>
> `default`
>
> :   Does nothing, and nothing can be restored (default).
>
> `copy`
>
> :   When applying a profile, copy the old values of all profile
>     options to a backup before setting them from the profile. These
>     options are reset to their old values using the backup when
>     restoring.
>
>     Every profile has its own list of backed up values. If the backup
>     already exists (e.g. if `apply-profile name` was called more than
>     once in a row), the existing backup is no changed. The restore
>     operation will remove the backup.
>
>     It's important to know that restoring does not "undo" setting an
>     option, but simply copies the old option value. Consider for
>     example `vf-add`, appends an entry to `vf`. This mechanism will
>     simply copy the entire `vf` list, and does
>     <span id="not">not</span>\_ execute the inverse of `vf-add` (that
>     would be `vf-remove`) on restoring.
>
>     Note that if a profile contains recursive profiles (via the
>     `profile` option), the options in these recursive profiles are
>     treated as if they were part of this profile. The referenced
>     profile's backup list is not used when creating or using the
>     backup. Restoring a profile does not restore referenced profiles,
>     only the options of referenced profiles (as if they were part of
>     the main profile).
>
> `copy-equal`
>
> :   Similar to `copy`, but restore an option only if it has the same
>     value as the value effectively set by the profile. This tries to
>     deal with the situation when the user does not want the option to
>     be reset after interactively changing it.

<div class="admonition" markdown="1">

Example

    [something]
    profile-restore=copy-equal
    vf-add=rotate=PI/2  # rotate by 90 degrees

Then running these commands will result in behavior as commented:

    set vf vflip
    apply-profile something
    vf add hflip
    apply-profile something
    # vf == vflip,rotate=PI/2,hflip,rotate=PI/2
    apply-profile something restore
    # vf == vflip

</div>

#### Conditional auto profiles

Profiles which have the `profile-cond` option set are applied
automatically if the associated condition matches (unless auto profiles
are disabled). The option takes a string, which is interpreted as Lua
expression. If the expression evaluates as truthy, the profile is
applied. If the expression errors or evaluates as falsy, the profile is
not applied. This Lua code execution is not sandboxed.

Any variables in condition expressions can reference properties. If an
identifier is not already defined by Lua or mpv, it is interpreted as
property. For example, `pause` would return the current pause status.
You cannot reference properties with `-` this way since that would
denote a subtraction, but if the variable name contains any `_`
characters, they are turned into `-`. For example, `playback_time` would
return the property `playback-time`.

A more robust way to access properties is using `p.property_name` or
`get("property-name", default_value)`. The automatic variable to
property magic will break if a new identifier with the same name is
introduced (for example, if a function named `pause()` were added,
`pause` would return a function value instead of the value of the
`pause` property).

Note that if a property is not available, it will return `nil`, which
can cause errors if used in expressions. These are logged in verbose
mode, and the expression is considered to be false.

Whenever a property referenced by a profile condition changes, the
condition is re-evaluated. If the return value of the condition changes
from falsy or error to truthy, the profile is applied.

This mechanism tries to "unapply" profiles once the condition changes
from truthy to falsy or error. If you want to use this, you need to set
`profile-restore` for the profile. Another possibility it to create
another profile with an inverse condition to undo the other profile.

Recursive profiles can be used. But it is discouraged to reference other
conditional profiles in a conditional profile, since this can lead to
tricky and unintuitive behavior.

<div class="admonition" markdown="1">

Example

Make only HD video look funny:

    [something]
    profile-desc=HD video sucks
    profile-cond=width >= 1280
    hue=-50

Make only videos containing "youtube" or "youtu.be" in their path
brighter:

    [youtube]
    profile-cond=path:find('youtu%.?be')
    gamma=20

If you want the profile to be reverted if the condition goes to false
again, you can set `profile-restore`:

    [something]
    profile-desc=Mess up video when entering fullscreen
    profile-cond=fullscreen
    profile-restore=copy
    vf-add=rotate=PI/2  # rotate by 90 degrees

This appends the `rotate` filter to the video filter chain when entering
fullscreen. When leaving fullscreen, the `vf` option is set to the value
it had before entering fullscreen. Note that this would also remove any
other filters that were added during fullscreen mode by the user.
Avoiding this is trickier, and could for example be solved by adding a
second profile with an inverse condition and operation:

    [something]
    profile-cond=fullscreen
    vf-add=@rot:rotate=PI/2

    [something-inv]
    profile-cond=not fullscreen
    vf-remove=@rot

</div>

<div class="warning" markdown="1">

<div class="title" markdown="1">

Warning

</div>

Every time an involved property changes, the condition is evaluated
again. If your condition uses `p.playback_time` for example, the
condition is re-evaluated approximately on every video frame. This is
probably slow.

</div>

This feature is managed by an internal Lua script. Conditions are
executed as Lua code within this script. Its environment contains at
least the following things:

`(function environment table)`

:   Every Lua function has an environment table. This is used for
    identifier access. There is no named Lua symbol for it; it is
    implicit.

    The environment does "magic" accesses to mpv properties. If an
    identifier is not already defined in `_G`, it retrieves the mpv
    property of the same name. Any occurrences of `_` in the name are
    replaced with `-` before reading the property. The returned value is
    as retrieved by `mp.get_property_native(name)`. Internally, a cache
    of property values, updated by observing the property is used
    instead, so properties that are not observable will be stuck at the
    initial value forever.

    If you want to access properties, that actually contain `_` in the
    name, use `get()` (which does not perform transliteration).

    Internally, the environment table has a `__index` meta method set,
    which performs the access logic.

`p`

:   A "magic" table similar to the environment table. Unlike the latter,
    this does not prefer accessing variables defined in `_G` - it always
    accesses properties.

`get(name [, def])`

:   Read a property and return its value. If the property value is `nil`
    (e.g. if the property does not exist), `def` is returned.

    This is superficially similar to `mp.get_property_native(name)`. An
    important difference is that this accesses the property cache, and
    enables the change detection logic (which is essential to the
    dynamic runtime behavior of auto profiles). Also, it does not return
    an error value as second return value.

    The "magic" tables mentioned above use this function as backend. It
    does not perform the `_` transliteration.

In addition, the same environment as in a blank mpv Lua script is
present. For example, `math` is defined and gives access to the Lua
standard math library.

<div class="warning" markdown="1">

<div class="title" markdown="1">

Warning

</div>

This feature is subject to change indefinitely. You might be forced to
adjust your profiles on mpv updates.

</div>

#### Legacy auto profiles

Some profiles are loaded automatically using a legacy mechanism. The
following example demonstrates this:

<div class="admonition" markdown="1">

Auto profile loading

    [extension.mkv]
    profile-desc="profile for .mkv files"
    vf=vflip

</div>

The profile name follows the schema `type.name`, where type can be
`protocol` for the input/output protocol in use (see
`--list-protocols`), and `extension` for the extension of the path of
the currently played file (*not* the file format).

This feature is very limited, and is considered soft-deprecated. Use
conditional auto profiles.

