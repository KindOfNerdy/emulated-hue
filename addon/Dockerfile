# Fork add-on: take the released 0.3.0 image (dependencies, s6 init scripts, /app)
# and replace only the emulated_hue package with the code from the fork.
# No BUILD_FROM: the Supervisor no longer passes it by default.
FROM ghcr.io/hass-emulated-hue/core:0.3.0

ARG FORK_REPO=KindOfNerdy/emulated-hue
ARG FORK_REF=light-id-and-label-filter
# The Supervisor passes BUILD_VERSION (= "version" in config.json). Using it in the
# RUN below invalidates the layer cache, so bump the version to fetch new code.
ARG BUILD_VERSION=unknown

RUN set -x \
    && echo "Installing ${FORK_REPO}@${FORK_REF} for add-on version ${BUILD_VERSION}" \
    && curl -fsSL -o /tmp/fork.tar.gz \
        "https://github.com/${FORK_REPO}/archive/${FORK_REF}.tar.gz" \
    && mkdir -p /tmp/fork \
    && tar -xzf /tmp/fork.tar.gz --strip-components=1 -C /tmp/fork \
    && test -f /tmp/fork/emulated_hue/__main__.py \
    && rm -rf /app/emulated_hue \
    && mv /tmp/fork/emulated_hue /app/emulated_hue \
    && rm -rf /tmp/fork /tmp/fork.tar.gz
