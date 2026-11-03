# Emulated HUE (Fork)

Fork of [hass-emulated-hue/core](https://github.com/hass-emulated-hue/core) for
using Home Assistant lights as an Ambilight+Hue extension.

Differences to the official add-on:

- New lights get the lowest free light ID instead of `max + 1`.
- Optional `include_labels` filter: only lights carrying a given Home Assistant
  label are exported.

It ships its own image (`ghcr.io/kindofnerdy/emulated-hue`, amd64 and aarch64),
built and security-scanned from this repository. Do not run it at the same time
as the official add-on (same ports).
