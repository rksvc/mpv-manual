#!/usr/bin/env bash
if [ ! -e mpv ]; then
    git clone --depth 1 -b release/0.41 https://github.com/mpv-player/mpv
fi
find docs -name '*.md' -type f -delete
pandoc mpv/DOCS/man/mpv.rst --lua-filter filter.lua
