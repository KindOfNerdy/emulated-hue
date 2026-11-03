# Emulated HUE (Fork)

Options: `http_port`, `https_port`, `use_default_ports_for_discovery`, `verbose`
(as in the official add-on) and `include_labels` (see below).

## Lowest free light ID

A new light gets the lowest unused ID instead of `max + 1`. Existing entries
and IDs are not changed.

## Label filter (`include_labels`)

Only export lights that carry one of these Home Assistant labels. Set the
add-on option `include_labels` (comma separated, e.g. `ambilight`), or add a
top-level key to `emulated_hue.json`:

```json
"include_labels": ["ambilight"]
```

- The add-on option wins if both are set. Empty and no key means all lights are exported (as before).
- Use the label ID (e.g. `ambilight`), not the display name.
- Only labels set on the light entity itself count, not labels of its device or area.
- Filtered-out lights keep their entries and IDs in the JSON.
- The labels are read when the add-on starts. Restart the add-on after
  changing labels in Home Assistant or this option.
- The log shows `include_labels [...]: exporting N of M lights` at startup.
- Room groups built from Home Assistant areas ignore the filter.

## Updating the code

The Dockerfile downloads the fork branch when the add-on is built. Bump
`version` in `addon/config.json` to build again with the latest code.
