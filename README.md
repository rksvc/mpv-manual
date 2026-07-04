## Build

```sh
git submodule update --init --depth 1
pandoc mpv/DOCS/man/mpv.rst --lua-filter filter.lua
```
