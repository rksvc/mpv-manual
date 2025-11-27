---
title: Using mpv from other programs or scripts
---

There are three choices for using mpv from other programs or scripts:

> 1.  Calling it as UNIX process. If you do this, *do not parse terminal
>     output*. The terminal output is intended for humans, and may
>     change any time. In addition, terminal behavior itself may change
>     any time. Compatibility cannot be guaranteed.
>
>     Your code should work even if you pass `--terminal=no`. Do not
>     attempt to simulate user input by sending terminal control codes
>     to mpv's stdin. If you need interactive control, using
>     `--input-ipc-server` or `--input-ipc-client` is recommended. This
>     gives you access to the [JSON IPC](json-ipc.md) over unix domain
>     sockets (or named pipes on Windows).
>
>     Depending on what you do, passing `--no-config` or `--config-dir`
>     may be a good idea to avoid conflicts with the normal mpv user
>     configuration intended for CLI playback.
>
>     Using `--input-ipc-server` or `--input-ipc-client` is also
>     suitable for purposes like remote control (however, the IPC
>     protocol itself is not "secure" and not intended to be so).
>
> 2.  Using libmpv. This is generally recommended when mpv is used as
>     playback backend for a completely different application. The
>     provided C API is very close to CLI mechanisms and the scripting
>     API.
>
>     Note that even though libmpv has different defaults, it can be
>     configured to work exactly like the CLI player (except command
>     line parsing is unavailable).
>
>     See [EMBEDDING INTO OTHER PROGRAMS
>     (LIBMPV)](embedding-into-other-programs-libmpv.md).
>
> 3.  As a user script ([LUA SCRIPTING](lua-scripting.md),
>     [JAVASCRIPT](javascript.md), [C PLUGINS](c-plugins.md)). This is
>     recommended when the goal is to "enhance" the CLI player. Scripts
>     get access to the entire client API of mpv.
>
>     This is the standard way to create third-party extensions for the
>     player.

All these access the client API, which is the sum of the various
mechanisms provided by the player core, as documented here:
[OPTIONS](options.md), [List of Input Commands](command-interface/list-of-input-commands.md),
[Properties](command-interface/properties.md), [List of events](command-interface/list-of-events.md) (also see C
API), [Hooks](command-interface/hooks.md).

