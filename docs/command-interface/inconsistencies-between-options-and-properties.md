---
title: Inconsistencies between options and properties
---

You can access (almost) all options as properties, though there are some
caveats with some properties (due to historical reasons):

`vid`, `aid`, `sid`

:   While playback is active, these return the actually active tracks.
    For example, if you set `aid=5`, and the currently played file
    contains no audio track with ID 5, the `aid` property will return
    `no`.

    Before mpv 0.31.0, you could set existing tracks at runtime only.

`display-fps`

:   This inconsistent behavior is deprecated. Post-deprecation, the
    reported value and the option value are cleanly separated
    (`override-display-fps` for the option value).

`vf`, `af`

:   If you set the properties during playback, and the filter chain
    fails to reinitialize, the option will be set, but the runtime
    filter chain does not change. On the other hand, the next video to
    be played will fail, because the initial filter chain cannot be
    created.

    This behavior changed in mpv 0.31.0. Before this, the new value was
    rejected *iff* a video (for `vf`) or an audio (for `af`) track was
    active. If playback was not active, the behavior was the same as the
    current one.

`playlist`

:   The property is read-only and returns the current internal playlist.
    The option is for loading playlist during command line parsing. For
    client API uses, you should use the `loadlist` command instead.

`profile`, `include`

:   These are write-only, and will perform actions as they are written
    to, exactly as if they were used on the mpv CLI commandline. Their
    only use is when using libmpv before `mpv_initialize()`, which in
    turn is probably only useful in encoding mode. Normal libmpv users
    should use other mechanisms, such as the `apply-profile` command,
    and the `mpv_load_config_file` API function. Avoid these properties.

