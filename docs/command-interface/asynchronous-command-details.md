---
title: Asynchronous command details
---

On the API level, every asynchronous command is bound to the context
which started it. For example, an asynchronous command started by
`mpv_command_async` is bound to the `mpv_handle` passed to the function.
Only this `mpv_handle` receives the completion notification
(`MPV_EVENT_COMMAND_REPLY`), and only this handle can abort a still
running command directly. If the `mpv_handle` is destroyed, any still
running async. commands started by it are terminated.

The scripting APIs and JSON IPC give each script/connection its own
implicit `mpv_handle`.

If the player is closed, the core may abort all pending async. commands
on its own (like a forced `mpv_abort_async_command()` call for each
pending command on behalf of the API user). This happens at the same
time `MPV_EVENT_SHUTDOWN` is sent, and there is no way to prevent this.

