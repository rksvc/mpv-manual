---
title: input.conf syntax
---

`[Shift+][Ctrl+][Alt+][Meta+]<key> [{<section>}] <command> ( ; <command> )*`

Note that by default, the right Alt key can be used to create special
characters, and thus does not register as a modifier. This can be
changed with `--input-right-alt-gr` option.

Newlines always start a new binding. `#` starts a comment (outside of
quoted string arguments). To bind commands to the `#` key, `SHARP` can
be used.

`<key>` is either the literal character the key produces (ASCII or
Unicode character), or a symbolic name (as printed by
`--input-keylist`).

`<section>` (braced with `{` and `}`) is the input section for this
command.

`<command>` is the command itself. It consists of the command name and
multiple (or none) arguments, all separated by whitespace. String
arguments should be quoted, typically with `"`. See
`Flat command syntax`.

You can bind multiple commands to one key. For example:

a show-text "command 1" ; show-text "command 2"

It's also possible to bind a command to a sequence of keys:

a-b-c show-text "command run after a, b, c have been pressed"

(This is not shown in the general command syntax.)

If `a` or `a-b` or `b` are already bound, this will run the first
command that matches, and the multi-key command will never be called.
Intermediate keys can be remapped to `ignore` in order to avoid this
issue. The maximum number of (non-modifier) keys for combinations is
currently 4.

