---
title: Commands specified as arrays
---

This applies to certain APIs, such as `mp.commandv()` or
`mp.command_native()` (with array parameters) in Lua scripting, or
`mpv_command()` or `mpv_command_node()` (with MPV_FORMAT_NODE_ARRAY) in
the C libmpv client API.

The command as well as all arguments are passed as a single array.
Similar to the [Flat command syntax](flat-command-syntax.md), you can
first pass prefixes as strings (each as separate array item), then the
command name as string, and then each argument as string or a native
value.

Since these APIs pass arguments as separate strings or native values,
they do not expect quotes, and do support escaping. Technically, there
is the input.conf parser, which first splits the command string into
arguments, and then invokes argument parsers for each argument. The
input.conf parser normally handles quotes and escaping. The array
command APIs mentioned above pass strings directly to the argument
parsers, or can sidestep them by the ability to pass non-string values.

Property expansion is disabled by default for these APIs. This can be
changed with the `expand-properties` prefix. See [Input Command
Prefixes](input-command-prefixes.md).

Sometimes commands have string arguments, that in turn are actually
parsed by other components (e.g. filter strings with `vf add`) - in
these cases, you you would have to double-escape in input.conf, but not
with the array APIs.

For complex commands, consider using [Named arguments](named-arguments.md)
instead, which should give slightly more compatibility. Some commands do
not support named arguments and inherently take an array, though.

