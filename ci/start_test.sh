#!/usr/bin/env bash
# Start test: runs the add-on image against a fake Home Assistant (ci/fake_ha.py)
# and checks that the app connects, loads the full state and serves the Hue API.
#
# Usage: ci/start_test.sh <image> [token]
#   token defaults to the one the fake accepts; pass another to check that the
#   test fails (negative test).
set -uo pipefail

IMAGE="${1:?image required}"
TOKEN="${2:-ci-token}"
NET=ehue-ci
TIMEOUT=90
CI_DIR="$(cd "$(dirname "$0")" && pwd)"

cleanup() {
  docker rm -f ehue-app ehue-fakeha >/dev/null 2>&1
  docker network rm "$NET" >/dev/null 2>&1
}
fail() {
  echo "::error::Start test failed: $*"
  echo "----- fake Home Assistant log -----"; docker logs ehue-fakeha 2>&1 | tail -50
  echo "----- app log -----"; docker logs ehue-app 2>&1 | tail -150
  exit 1
}
trap cleanup EXIT
cleanup

docker network create "$NET" >/dev/null
docker run -d --name ehue-fakeha --network "$NET" \
  -v "$CI_DIR:/ci:ro" --entrypoint python "$IMAGE" /ci/fake_ha.py >/dev/null
docker run -d --name ehue-app --network "$NET" \
  -p 8080:80 -p 8443:443 \
  -e HASS_URL=http://ehue-fakeha:8123 -e HASS_TOKEN="$TOKEN" \
  -e DATA_DIR=/tmp/ehue-data -e VERBOSE=true \
  "$IMAGE" >/dev/null

# wait until both APIs answer with a bridge config
ready=false
for _ in $(seq 1 "$TIMEOUT"); do
  if ! docker ps -q -f name=ehue-app -f status=running | grep -q .; then
    fail "app container exited"
  fi
  http=$(curl -fs --max-time 2 http://localhost:8080/api/nouser/config || true)
  https=$(curl -fsk --max-time 2 https://localhost:8443/api/nouser/config || true)
  if jq -e '.bridgeid and .mac' <<<"$http" >/dev/null 2>&1 \
    && jq -e '.bridgeid and .mac' <<<"$https" >/dev/null 2>&1; then
    ready=true
    break
  fi
  sleep 1
done
[ "$ready" = true ] || fail "Hue API did not answer within ${TIMEOUT}s"
echo "Bridge config: $http"

curl -fs --max-time 5 -o /dev/null http://localhost:8080/description.xml \
  || fail "/description.xml not served"

app_log=$(docker logs ehue-app 2>&1)
ha_log=$(docker logs ehue-fakeha 2>&1)

for line in "Connected to Home Assistant" "Started HTTP webserver" "Started HTTPS webserver"; do
  grep -qF "$line" <<<"$app_log" || fail "missing log line: $line"
done
for bad in "Failed to create HTTP" "Cannot connect to Home Assistant" "Traceback"; do
  if grep -qF "$bad" <<<"$app_log"; then fail "error in app log: $bad"; fi
done
for cmd in subscribe_events get_states config/area_registry/list \
  config/device_registry/list config/entity_registry/list; do
  grep -qx "COMMAND $cmd" <<<"$ha_log" || fail "app did not request $cmd"
done

echo "Start test passed: app connected to the fake Home Assistant and serves the Hue API."
