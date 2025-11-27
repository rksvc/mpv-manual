#!/usr/bin/env bash
if [ ! -e mpv ]; then
    git clone --depth 1 -b release/0.40 https://github.com/mpv-player/mpv
fi
pandoc mpv/DOCS/man/mpv.rst -t markdown_mmd -o mpv.md
find docs -name '*.md' -type f -delete
python mdsplit.py mpv.md docs
mv docs/description.md docs/index.md
mv docs/command-interface.md docs/command-interface/index.md
rm mpv.md
