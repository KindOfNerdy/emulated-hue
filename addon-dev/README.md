# Emulated HUE (Fork, Dev)

Development build of the [Emulated HUE (Fork)](../addon/README.md) add-on. It
runs next to the production add-on with its own host ports (8080/8443), its own
data directory (`/config/hass-emulated-hue-dev`) and without host networking, so
TVs and Hue apps do not discover it. Use it to check that a new build starts and
connects to Home Assistant before it is released as "Emulated HUE (Fork)".

Versions `x.y.z-dev.N` are built from the `dev` branch of this repository and
are not released on GitHub.
