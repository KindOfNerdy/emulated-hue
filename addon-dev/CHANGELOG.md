# Changelog

## 0.4.0-dev.3

- With verbose logging, every exported light is logged at startup as the Hue API serves it (type and state), so an install can be checked without pairing.
- Start test: switches two lights through the Hue API and checks the Home Assistant service calls (turn_on with brightness and hs colour, turn_off).

## 0.4.0-dev.2

- pydantic 1.10 → 2.14: `EntityState` uses the pydantic 2 API; `hue_saturation` is stored as floats, as Home Assistant reports it (pydantic 2 no longer truncates fractional values to int).
- Start test: the fake Home Assistant now also serves an `hs` colour light with fractional `hs_color`.

## 0.4.0-dev.1

- First development build: same code as release 0.3.13, packaged with own host ports (8080/8443), own data directory and without host networking.
