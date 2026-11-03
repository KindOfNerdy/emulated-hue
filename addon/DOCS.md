# Emulated HUE (Fork)

Options are the same as in the official add-on: `http_port`, `https_port`,
`use_default_ports_for_discovery`, `verbose`.

The data is stored in `/config/hass-emulated-hue/emulated_hue.json`, the same
file the official add-on uses. Make a backup before switching.

## Lowest free light ID

A new light gets the lowest unused ID instead of `max + 1`. Existing entries
and IDs are not changed.

## Label filter (`include_labels`)

Add a top-level key to `emulated_hue.json`:

```json
"include_labels": ["ambilight"]
```

- Use the label ID (e.g. `ambilight`), not the display name.
- Only labels set on the light entity itself count, not labels of its device or area.
- Without the key, all lights are exported (as before).
- Filtered-out lights keep their entries and IDs in the JSON.
- The labels are read when the add-on starts. Restart the add-on after
  changing labels in Home Assistant or the key in the JSON.
- The log shows `include_labels [...]: exporting N of M lights` at startup.

## Updating the code

The Dockerfile downloads the fork branch when the add-on is built. Bump
`version` in `addon/config.json` to build again with the latest code.
