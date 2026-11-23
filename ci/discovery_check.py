"""
Discovery check for the CI start test.

Runs in a second container on the same Docker network as the app and checks both
ways clients find the emulated bridge:
- mDNS: a `_hue._tcp.local.` service whose `bridgeid` property matches
- SSDP: an answer to an M-SEARCH on 239.255.255.250:1900 with `IpBridge` and the
  same `hue-bridgeid`

Usage: python discovery_check.py <bridgeid>
Prints "MDNS ok ..." / "SSDP ok ..." and exits non-zero if one of them fails.
"""

import socket
import sys
import time

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

HUE_TYPE = "_hue._tcp.local."
TIMEOUT = 15


def check_mdns(bridge_id: str) -> bool:
    """Browse for the Hue service and compare its bridgeid property."""
    found: list[str] = []

    def on_change(zeroconf, service_type, name, state_change):  # noqa: ARG001
        if state_change is ServiceStateChange.Added:
            found.append(name)

    zc = Zeroconf()
    try:
        ServiceBrowser(zc, HUE_TYPE, handlers=[on_change])
        deadline = time.monotonic() + TIMEOUT
        while time.monotonic() < deadline:
            for name in list(found):
                info = zc.get_service_info(HUE_TYPE, name, timeout=3000)
                if not info:
                    continue
                props = {
                    k.decode(): (v.decode() if isinstance(v, bytes) else v)
                    for k, v in info.properties.items()
                }
                print(f"MDNS found {name} port={info.port} props={props}", flush=True)
                if props.get("bridgeid", "").upper() == bridge_id.upper() and info.port == 443:
                    print("MDNS ok", flush=True)
                    return True
            time.sleep(0.5)
    finally:
        zc.close()
    print(f"MDNS failed: services seen {found}", flush=True)
    return False


def check_ssdp(bridge_id: str) -> bool:
    """Send an M-SEARCH and look for the bridge's answer."""
    msg = (
        b"M-SEARCH * HTTP/1.1\r\n"
        b"HOST: 239.255.255.250:1900\r\n"
        b'MAN: "ssdp:discover"\r\n'
        b"MX: 2\r\n"
        b"ST: ssdp:all\r\n\r\n"
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.settimeout(1)
    answers = []
    deadline = time.monotonic() + TIMEOUT
    try:
        while time.monotonic() < deadline:
            sock.sendto(msg, ("239.255.255.250", 1900))
            end = time.monotonic() + 2
            while time.monotonic() < end:
                try:
                    data, addr = sock.recvfrom(2048)
                except TimeoutError:
                    continue
                text = data.decode(errors="replace")
                answers.append(text)
                if "IpBridge" in text and f"hue-bridgeid: {bridge_id}".upper() in text.upper():
                    first = text.splitlines()[0] if text else ""
                    print(f"SSDP ok from {addr[0]}: {first}", flush=True)
                    return True
    finally:
        sock.close()
    print(f"SSDP failed: {len(answers)} answers, first: {answers[:1]}", flush=True)
    return False


def main() -> None:
    """Run both checks."""
    bridge_id = sys.argv[1]
    mdns = check_mdns(bridge_id)
    ssdp = check_ssdp(bridge_id)
    sys.exit(0 if mdns and ssdp else 1)


if __name__ == "__main__":
    main()
