# Changelog

## 0.4.0-dev.6

- Updated: python-slugify 7.0.0 → 9.2.0, hass-client 0.1.5 → 0.1.6 (no more hanging when Home Assistant cannot be reached).
- Fix: brightness reported to Hue clients is capped at 254 (Home Assistant goes up to 255).
- Fix: the saved light state is used again at startup until Home Assistant reports the current one; an invalid saved state is ignored with a warning.

## 0.4.0-dev.5

- Updated: uvloop 0.17.0 → 0.23.0, getmac 0.8.3 → 0.9.6, tzlocal 4.2 → 5.4.5, aiorun 2022.11.1 → 2025.1.1, netaddr 0.8.0 → 1.3.0.

## 0.4.0-dev.4

- zeroconf 0.47.4 → 0.154.0 (fixes the open security advisories); mDNS registration unchanged.
- Start test: checks that the bridge answers mDNS (`_hue._tcp.local.`) and SSDP with its bridge id.

## 0.4.0-dev.3

- With verbose logging, every exported light is logged at startup as the Hue API serves it (type and state), so an install can be checked without pairing.
- Start test: switches two lights through the Hue API and checks the Home Assistant service calls (turn_on with brightness and hs colour, turn_off).

## 0.4.0-dev.2

- pydantic 1.10 → 2.14: `EntityState` uses the pydantic 2 API; `hue_saturation` is stored as floats, as Home Assistant reports it (pydantic 2 no longer truncates fractional values to int).
- Start test: the fake Home Assistant now also serves an `hs` colour light with fractional `hs_color`.

## 0.4.0-dev.1

- First development build: same code as release 0.3.13, packaged with own host ports (8080/8443), own data directory and without host networking.
