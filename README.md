## Build

```sh
git clone --depth 1 -b release/0.41 https://github.com/mpv-player/mpv
pandoc mpv/DOCS/man/mpv.rst --lua-filter filter.lua
```
