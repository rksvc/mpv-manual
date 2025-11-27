---
title: Input Sections
---

Input sections group a set of bindings, and enable or disable them at
once. In `input.conf`, each key binding is assigned to an input section,
rather than actually having explicit text sections.

See also: `enable-section` and `disable-section` commands.

Predefined bindings:

`default`

:   Bindings without input section are implicitly assigned to this
    section. It is enabled by default during normal playback.

`encode`

:   Section which is active in encoding mode. It is enabled exclusively,
    so that bindings in the `default` sections are ignored.

