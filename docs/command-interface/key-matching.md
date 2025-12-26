---
title: Key matching
---

mpv maintains key press history. If the current key completes one or
more bound sequences (including single-key bindings), then mpv chooses
the longest. If this sequence is bound to `ignore`, then tracking
continues as if nothing was matched. Otherwise, it triggers the command
bound to this sequence and clears the key history.

Note that while single-key bindings override builtin bindings, this is
not the case with multi-key sequences. For example, a `b-c` sequence in
input.conf would be overridden by a builtin binding `b`. In this case,
if you don't care about `b`, you can bind it to `ignore`.

As a more complex example, if you want to bind both `b` and `a-b-c`,
then it won't work, because `b` would override `a-b-c`. However, binding
`a-b` to `ignore` would allow that, because after `a-b` the longest
match `a-b` is ignored, and a following `c` would trigger the sequence
`a-b-c` while `b` alone would still work.

