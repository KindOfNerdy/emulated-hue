# Emulated HUE (Fork, Dev)

Same code base as "Emulated HUE (Fork)", packaged for testing next to it.

## Differences to the production add-on

- No host networking: the Hue API is published on host ports 8080 (HTTP) and
  8443 (HTTPS), changeable in the add-on's network settings. Discovery
  (mDNS/SSDP) stays inside the container network, so TVs and Hue apps do not
  see a second bridge. Do not pair anything with it.
- Own data directory (option `data`, default `/config/hass-emulated-hue-dev`).
  The production files in `/config/hass-emulated-hue` are not touched.
- Starts manually only (`boot: manual`), verbose logging is on by default.
- Versions are `x.y.z-dev.N`, built from the `dev` branch. There is no GitHub
  release; the add-on store shows a new version as an update.

## Options

- `data`: directory for `emulated_hue.json` and the certificates.
- `include_labels`: same filter as in the production add-on (comma separated
  Home Assistant label IDs, e.g. `ambilight`). Empty exports all lights.
- `verbose`: debug logging.

## What to check after a start

- Log: `Connected to Home Assistant`, `Started HTTP webserver on port 80`,
  `Started HTTPS webserver on port 443`, no `Traceback`.
- `http://<home-assistant-host>:8080/api/nouser/config` answers with a bridge
  config (`bridgeid`, `mac`). The `bridgeid` differs from the production
  add-on because the container has its own MAC address.
- With `include_labels` set: `exporting N of M lights` in the log.
