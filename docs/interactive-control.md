---
title: Interactive Control
---

mpv has a fully configurable, command-driven control layer which allows
you to control mpv using keyboard, mouse, or remote control (there is no
LIRC support - configure remotes as input devices instead).

See the `--input-` options for ways to customize it.

The following listings are not necessarily complete. See
`etc/input.conf` in the mpv source files for a list of default bindings.
User `input.conf` files and Lua scripts can define additional key
bindings.

See [COMMAND INTERFACE](command-interface.md) and [Key names](command-interface/key-names.md)
sections for more details on configuring keybindings.

See also `--input-test` for interactive binding details by key, and the
[stats](stats.md) built-in script for key bindings list (including print
to terminal). By default, the ? key toggles the display of this list.

#### Keyboard Control

LEFT and RIGHT

:   Seek backward/forward 5 seconds. Shift+arrow does a 1 second exact
    seek (see `--hr-seek`).

UP and DOWN

:   Seek forward/backward 1 minute. Shift+arrow does a 5 second exact
    seek (see `--hr-seek`).

Ctrl+LEFT and Ctrl+RIGHT

:   Seek to the previous/next subtitle. Subject to some restrictions and
    might not always work; see `sub-seek` command.

Ctrl+Shift+LEFT and Ctrl+Shift+RIGHT

:   Adjust subtitle delay so that the previous or next subtitle is
    displayed now. This is especially useful to sync subtitles to audio.

\[ and \]

:   Decrease/increase current playback speed by 10%.

{ and }

:   Halve/double current playback speed.

BACKSPACE

:   Reset playback speed to normal.

Shift+BACKSPACE

:   Undo the last seek. This works only if the playlist entry was not
    changed. Hitting it a second time will go back to the original
    position. See `revert-seek` command for details.

Shift+Ctrl+BACKSPACE

:   Mark the current position. This will then be used by
    `Shift+BACKSPACE` as revert position (once you seek back, the marker
    will be reset). You can use this to seek around in the file and then
    return to the exact position where you left off.

\< and \>

:   Go backward/forward in the playlist.

ENTER

:   Go forward in the playlist.

Shift+HOME and Shift+END

:   Go to the first/last playlist entry.

p and SPACE

:   Pause (pressing again unpauses).

.

:   Step forward. Pressing once will pause, every consecutive press will
    play one frame and then go into pause mode again.

,

:   Step backward. Pressing once will pause, every consecutive press
    will play one frame in reverse and then go into pause mode again.

q

:   Stop playing and quit.

Q

:   Like `q`, but store the current playback position. Playing the same
    file later will resume at the old playback position if possible. See
    [RESUMING PLAYBACK](resuming-playback.md).

/ and \*

:   Decrease/increase volume.

KP_DIVIDE and KP_MULTIPLY

:   Decrease/increase volume.

9 and 0

:   Decrease/increase volume.

m

:   Mute sound.

\_

:   Cycle through the available video tracks.

\#

:   Cycle through the available audio tracks.

E

:   Cycle through the available Editions.

f

:   Toggle fullscreen (see also `--fs`).

ESC

:   Exit fullscreen mode.

T

:   Toggle stay-on-top (see also `--ontop`).

w and W

:   Decrease/increase pan-and-scan range. The `e` key does the same as
    `W` currently, but use is discouraged. See `--panscan` for more
    information.

o and P

:   Show progression bar, elapsed time and total duration on the OSD.

O

:   Toggle OSD states between normal and playback time/duration.

v

:   Toggle subtitle visibility.

j and J

:   Cycle through the available subtitles.

z and Z

:   Adjust subtitle delay by -/+ 0.1 seconds. The `x` key does the same
    as `Z` currently, but use is discouraged.

l

:   Set/clear A-B loop points. See `ab-loop` command for details.

L

:   Toggle infinite looping.

Ctrl++ and Ctrl+- Adjust audio delay (A/V sync) by +/- 0.1 seconds.

Ctrl+KP_ADD and Ctrl+KP_SUBTRACT

:   Adjust audio delay (A/V sync) by +/- 0.1 seconds.

G and F

:   Adjust subtitle font size by +/- 10%.

u

:   Switch between applying only `--sub-ass-*` overrides (default) to
    SSA/ASS subtitles, and overriding them almost completely with the
    normal subtitle style. See `--sub-ass-override` for more info.

V

:   Cycle through which video data gets used for ASS rendering. See
    `--sub-ass-use-video-data` for more info.

r and R

:   Move subtitles up/down. The `t` key does the same as `R` currently,
    but use is discouraged.

s

:   Take a screenshot.

S

:   Take a screenshot, without subtitles. (Whether this works depends on
    VO driver support.)

Ctrl+s

:   Take a screenshot, as the window shows it (with subtitles, OSD, and
    scaled video).

HOME

:   Seek to the beginning of the file.

PGUP and PGDWN

:   Seek to the beginning of the previous/next chapter. In most cases,
    "previous" will actually go to the beginning of the current chapter;
    see `--chapter-seek-threshold`.

Shift+PGUP and Shift+PGDWN

:   Seek backward or forward by 10 minutes. (This used to be mapped to
    PGUP/PGDWN without Shift.)

b

:   Activate/deactivate debanding.

d

:   Cycle the deinterlacing filter.

A

:   Cycle aspect ratio override.

Ctrl+h

:   Toggle hardware video decoding on/off.

Alt+LEFT, Alt+RIGHT, Alt+UP, Alt+DOWN

:   Move the video rectangle (panning).

Alt++ and Alt+- Change video zoom.

Alt+KP_ADD and Alt+KP_SUBTRACT

:   Change video zoom.

Alt+BACKSPACE

:   Reset the pan/zoom settings.

F8

:   Show the playlist and the current position in it.

F9

:   Show the list of audio and subtitle streams.

Ctrl+v

:   Append the file or URL in the clipboard to the playlist. If nothing
    is currently playing, it is played immediately. Only works on
    platforms that support the `clipboard` property.

i and I

:   Show/toggle an overlay displaying statistics about the currently
    playing file such as codec, framerate, number of dropped frames and
    so on. See [STATS](stats.md) for more information.

?

:   Toggle an overlay displaying the active key bindings. See
    [STATS](stats.md) for more information.

DEL

:   Cycle OSC visibility between never / auto (mouse-move) / always

\`

:   Show the console. (ESC closes it again. See [CONSOLE](console.md).)

(The following keys are valid only when using a video output that
supports the corresponding adjustment.)

1 and 2

:   Adjust contrast.

3 and 4

:   Adjust brightness.

5 and 6

:   Adjust gamma.

7 and 8

:   Adjust saturation.

Alt+0 (and Command+0 on macOS)

:   Resize video window to half its original size.

Alt+1 (and Command+1 on macOS)

:   Resize video window to its original size.

Alt+2 (and Command+2 on macOS)

:   Resize video window to double its original size.

Command + f (macOS only)

:   Toggle fullscreen (see also `--fs`).

(The following keybindings open a menu in the console that lets you
choose from a list of items by typing part of the desired item, by
clicking the desired item, or by navigating them with keybindings:
`Down` and `Ctrl+n` go down, `Up` and `Ctrl+p` go up, `Page down` and
`Ctrl+f` scroll down one page, and `Page up` and `Ctrl+b` scroll up one
page.)

In track menus, selecting the current tracks disables it.

g-p

:   Select a playlist entry.

g-s

:   Select a subtitle track.

g-S

:   Select a secondary subtitle track.

g-a

:   Select an audio track.

g-v

:   Select a video track.

g-t

:   Select a track of any type.

g-c

:   Select a chapter.

g-e

:   Select an MKV edition or DVD/Blu-ray title.

g-l

:   Select a subtitle line to seek to. This currently requires `ffmpeg`
    in `PATH`, or in the same folder as mpv on Windows.

g-d

:   Select an audio device.

g-h

:   Select a file from the watch history. Requires
    `--save-watch-history`.

g-w

:   Select a file from watch later config files (see [RESUMING
    PLAYBACK](resuming-playback.md)) to resume playing. Requires
    `--write-filename-in-watch-later-config`.

g-b

:   Select a defined input binding.

g-r

:   Show the values of all properties.

g-m, MENU, Ctrl+p

:   Show a menu with miscellaneous entries.

See [SELECT](select.md) for more information.

(The following keys are valid if you have a keyboard with multimedia
keys.)

PAUSE

:   Pause.

STOP

:   Stop playing and quit.

PREVIOUS and NEXT

:   Seek backward/forward 1 minute.

ZOOMIN and ZOOMOUT

:   Change video zoom.

If you miss some older key bindings, look at
`etc/restore-old-bindings.conf` in the mpv git repository.

#### Mouse Control

Ctrl+left click

:   Pan while holding the button, keeping the clicked part of the video
    under the cursor.

Left double click

:   Toggle fullscreen on/off.

Right click

:   Toggle pause on/off.

Forward/Back button

:   Skip to next/previous entry in playlist.

Wheel up/down

:   Decrease/increase volume.

Wheel left/right

:   Seek forward/backward 10 seconds.

Ctrl+Wheel up/down

:   Change video zoom keeping the part of the video hovered by the
    cursor under it.

#### Context Menu

<div class="warning" markdown="1">

<div class="title" markdown="1">

Warning

</div>

This feature is experimental. It may not work with all VOs. A libass
based fallback may be implemented in the future.

</div>

Context Menu is a menu that pops up on the video window on user
interaction (mouse right click, etc.).

To use this feature, you need to fill the `menu-data` property with menu
definition data, and add a keybinding to run the `context-menu` command,
which can be done with a user script.

