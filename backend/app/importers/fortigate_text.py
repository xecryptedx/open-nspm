from __future__ import annotations

import re
from typing import Any


_QUOTED_VALUE_RE = re.compile(r'"([^"]+)"')


def _parse_list(line: str) -> list[str]:
    return _QUOTED_VALUE_RE.findall(line)


def parse(text: str) -> dict[str, Any]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    policies: list[dict[str, Any]] = []
    addresses: list[dict[str, Any]] = []

    context: str | None = None
    current: dict[str, Any] = {}

    for line in lines:
        if line.startswith("config firewall policy"):
            context = "policy"
            continue
        if line.startswith("config firewall address"):
            context = "address"
            continue
        if line == "end":
            context = None
            current = {}
            continue

        if line.startswith("edit"):
            if context == "policy":
                current = {"policyid": int(line.split()[1])}
                policies.append(current)
            elif context == "address":
                name = _QUOTED_VALUE_RE.search(line)
                current = {"name": name.group(1) if name else line.split()[1]}
                current["type"] = "ipmask"
                addresses.append(current)
            continue

        if line.startswith("next"):
            current = {}
            continue

        if context == "policy":
            if line.startswith("set srcintf"):
                current["srcintf"] = [{"name": value} for value in _parse_list(line)]
            elif line.startswith("set dstintf"):
                current["dstintf"] = [{"name": value} for value in _parse_list(line)]
            elif line.startswith("set srcaddr"):
                current["srcaddr"] = [{"name": value} for value in _parse_list(line)]
            elif line.startswith("set dstaddr"):
                current["dstaddr"] = [{"name": value} for value in _parse_list(line)]
            elif line.startswith("set service"):
                current["service"] = [{"name": value} for value in _parse_list(line)]
            elif line.startswith("set action"):
                current["action"] = line.split()[2]
            elif line.startswith("set status"):
                current["status"] = line.split()[2]
            elif line.startswith("set logtraffic"):
                current["logtraffic"] = line.split()[2]
            elif line.startswith("set schedule"):
                values = _parse_list(line)
                current["schedule"] = values[0] if values else line.split()[2]
            elif line.startswith("set uuid"):
                parts = line.split()
                current["uuid"] = parts[2] if len(parts) > 2 else None
            elif line.startswith("set nat"):
                current["nat"] = line.split()[2]
            elif line.startswith("set comments"):
                values = _parse_list(line)
                current["comments"] = values[0] if values else ""

        elif context == "address":
            if line.startswith("set subnet"):
                parts = line.split()
                if len(parts) >= 4:
                    current["subnet"] = f"{parts[2]} {parts[3]}"
            elif line.startswith("set type"):
                current["type"] = line.split()[2]
            elif line.startswith("set start-ip"):
                current["start-ip"] = line.split()[2]
            elif line.startswith("set end-ip"):
                current["end-ip"] = line.split()[2]
            elif line.startswith("set fqdn"):
                values = _parse_list(line)
                current["fqdn"] = values[0] if values else None

    return {"policies": policies, "addresses": addresses}
