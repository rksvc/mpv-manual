---
title: Named arguments
---

This applies to certain APIs, such as `mp.command_native()` (with tables
that have string keys) in Lua scripting, or `mpv_command_node()` (with
MPV_FORMAT_NODE_MAP) in the C libmpv client API.

The name of the command is provided with a `name` string field. The name
of each command is defined in each command description in the [List of
Input Commands](list-of-input-commands.md). `--input-cmdlist` also lists
them. See the `subprocess` command for an example.

Some commands do not support named arguments (e.g. `run` command). You
need to use APIs that pass arguments as arrays.

Named arguments are not supported in the "flat" input.conf syntax, which
means you cannot use them for key bindings in input.conf at all.

Property expansion is disabled by default for these APIs. This can be
changed with the `expand-properties` prefix. See [Input Command
Prefixes](input-command-prefixes.md).

