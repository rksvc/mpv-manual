#!/usr/bin/env bash
find docs -name '*.md' -type f -delete
pandoc mpv/DOCS/man/mpv.rst --lua-filter filter.lua
