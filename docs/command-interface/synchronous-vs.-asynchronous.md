---
title: Synchronous vs. Asynchronous
---

The `async` and `sync` prefix matter only for how the issuer of the
command waits on the completion of the command. Normally it does not
affect how the command behaves by itself. There are the following cases:

- Normal input.conf commands are always run asynchronously. Slow running
  commands are queued up or run in parallel.
- "Multi" input.conf commands (1 key binding, concatenated with `;`)
  will be executed in order, except for commands that are async (either
  prefixed with `async`, or async by default for some commands). The
  async commands are run in a detached manner, possibly in parallel to
  the remaining sync commands in the list.
- Normal Lua and libmpv commands (e.g. `mpv_command()`) are run in a
  blocking manner, unless the `async` prefix is used, or the command is
  async by default. This means in the sync case the caller will block,
  even if the core continues playback. Async mode runs the command in a
  detached manner.
- Async libmpv command API (e.g. `mpv_command_async()`) never blocks the
  caller, and always notify their completion with a message. The `sync`
  and `async` prefixes make no difference.
- Lua also provides APIs for running async commands, which behave
  similar to the C counterparts.
- In all cases, async mode can still run commands in a synchronous
  manner, even in detached mode. This can for example happen in cases
  when a command does not have an asynchronous implementation. The async
  libmpv API still never blocks the caller in these cases.

Before mpv 0.29.0, the `async` prefix was only used by screenshot
commands, and made them run the file saving code in a detached manner.
This is the default now, and `async` changes behavior only in the ways
mentioned above.

Currently the following commands have different waiting characteristics
with sync vs. async: sub-add, audio-add, sub-reload, audio-reload,
rescan-external-files, screenshot, screenshot-to-file, dump-cache,
ab-loop-dump-cache.

