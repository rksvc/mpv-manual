---
title: Input Command Prefixes
---

These prefixes are placed between key name and the actual command.
Multiple prefixes can be specified. They are separated by whitespace.

`osd-auto`

:   Use the default behavior for this command. This is the default for
    `input.conf` commands. Some libmpv/scripting/IPC APIs do not use
    this as default, but use `no-osd` instead.

`no-osd`

:   Do not use any OSD for this command.

`osd-bar`

:   If possible, show a bar with this command. Seek commands will show
    the progress bar, property changing commands may show the newly set
    value.

`osd-msg`

:   If possible, show an OSD message with this command. Seek command
    show the current playback time, property changing commands show the
    newly set value as text.

`osd-msg-bar`

:   Combine osd-bar and osd-msg.

`raw`

:   Do not expand properties in string arguments. (Like
    `"${property-name}"`.) This is the default for some
    libmpv/scripting/IPC APIs.

`expand-properties`

:   All string arguments are expanded as described in [Property
    Expansion](property-expansion.md). This is the default for
    `input.conf` commands.

`repeatable`

:   For some commands, keeping a key pressed doesn't run the command
    repeatedly. This prefix forces enabling key repeat in any case. For
    a list of commands: the first command determines the repeatability
    of the whole list (up to and including version 0.33 - a list was
    always repeatable).

`nonrepeatable`

:   For some commands, keeping a key pressed runs the command
    repeatedly. This prefix forces disabling key repeat in any case.

`nonscalable`

:   When some commands (e.g. `add`) are bound to scalable keys
    associated to a high-precision input device like a touchpad (e.g.
    `WHEEL_UP`), the value specified in the command is scaled to smaller
    steps based on the high resolution input data if available. This
    prefix forces disabling this behavior, so the value is always
    changed in the discrete unit specified in the key binding.

`async`

:   Allow asynchronous execution (if possible). Note that only a few
    commands will support this (usually this is explicitly documented).
    Some commands are asynchronous by default (or rather, their effects
    might manifest after completion of the command). The semantics of
    this flag might change in the future. Set it only if you don't rely
    on the effects of this command being fully realized when it returns.
    See [Synchronous vs. Asynchronous](synchronous-vs.-asynchronous.md).

`sync`

:   Allow synchronous execution (if possible). Normally, all commands
    are synchronous by default, but some are asynchronous by default for
    compatibility with older behavior.

All of the osd prefixes are still overridden by the global `--osd-level`
settings.

