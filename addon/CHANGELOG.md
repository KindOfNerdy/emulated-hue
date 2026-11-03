# Changelog

## 0.3.7

- The Home Assistant notification for a light with an ID above 63 now has a **Clean up now** link. It makes a backup of `emulated_hue.json`, removes light entries that are not exported (missing in Home Assistant or filtered out by `include_labels`), gives the light a free ID and restarts the add-on. A second notification confirms the result. Lights used in groups or scenes keep their ID.

## 0.3.6

- A new light that gets an ID above 63 now triggers a warning in the log and a Home Assistant notification with instructions. Some clients (e.g. a Philips TV for Ambilight+Hue) only list lights with an ID up to 63 (observed behaviour).

## 0.3.5

- Add names and descriptions (English, German) for all add-on options.
- Log the source of the active `include_labels` filter (add-on option or `emulated_hue.json`).
- If `emulated_hue.json` already contains `include_labels`, log the value to enter in the add-on option; warn with both lists if they differ (the add-on option wins).

## 0.3.4

- New add-on option `include_labels` (comma separated label IDs). It takes precedence over the `include_labels` key in `emulated_hue.json`.

## 0.3.3

- Mark the add-on as stable.
- Add icon and logo.

## 0.3.2

- New filter `include_labels` in `emulated_hue.json`: only export lights carrying one of the given Home Assistant labels. Without the key, all lights are exported as before.

## 0.3.1

- First release of the fork add-on, built on the official `0.3.0` image with the `emulated_hue` package from this fork.
- New lights get the lowest free light ID instead of `max + 1`.
