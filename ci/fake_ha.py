"""Minimal fake Home Assistant for the CI start test.

Speaks just enough of the websocket API for hass_client to connect and load the
full state: auth handshake, subscribe_events, get_states and the area, device and
entity registries. Every command type it receives is printed as "COMMAND <type>"
so the start test can check that the app really requested the full state.
"""
import json
import sys

from aiohttp import web

TOKEN = "ci-token"

AREA = {"area_id": "living_room", "name": "Living Room", "labels": []}
DEVICE = {"id": "dev1", "area_id": "living_room", "name": "Test Lamp"}
ENTITY = {
    "entity_id": "light.test",
    "device_id": "dev1",
    "area_id": None,
    "disabled_by": None,
    "labels": [],
}
STATE = {
    "entity_id": "light.test",
    "state": "on",
    "attributes": {
        "friendly_name": "Test Lamp",
        "brightness": 200,
        "color_mode": "brightness",
        "supported_color_modes": ["brightness"],
    },
    "last_changed": "2026-01-01T00:00:00+00:00",
    "last_updated": "2026-01-01T00:00:00+00:00",
    "context": {"id": "ci", "parent_id": None, "user_id": None},
}

RESULTS = {
    "subscribe_events": None,
    "get_states": [STATE],
    "config/area_registry/list": [AREA],
    "config/device_registry/list": [DEVICE],
    "config/entity_registry/list": [ENTITY],
}


def log(*args):
    print(*args, flush=True)


async def websocket(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await ws.send_json({"type": "auth_required", "ha_version": "2026.11.0"})
    auth = await ws.receive_json()
    if auth.get("type") != "auth" or auth.get("access_token") != TOKEN:
        log("AUTH_INVALID")
        await ws.send_json({"type": "auth_invalid", "message": "Invalid access token"})
        await ws.close()
        return ws
    log("AUTH_OK")
    await ws.send_json({"type": "auth_ok", "ha_version": "2026.11.0"})
    async for msg in ws:
        if msg.type != web.WSMsgType.TEXT:
            continue
        data = json.loads(msg.data)
        log("COMMAND", data.get("type"))
        await ws.send_json(
            {
                "id": data["id"],
                "type": "result",
                "success": True,
                "result": RESULTS.get(data.get("type")),
            }
        )
    return ws


async def post_state(request: web.Request) -> web.Response:
    return web.json_response({})


def main() -> None:
    app = web.Application()
    app.router.add_get("/api/websocket", websocket)
    app.router.add_post("/api/states/{entity_id}", post_state)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
    log(f"fake Home Assistant listening on {port}")
    web.run_app(app, port=port, print=None)


if __name__ == "__main__":
    main()
