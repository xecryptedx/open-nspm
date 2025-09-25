from __future__ import annotations

from ipaddress import ip_network
from typing import Any


def _normalize_address(address: dict[str, Any]) -> dict[str, Any]:
    addr_type = address.get("type", "ipmask")
    name = address.get("name")
    tags = address.get("tagging", [])
    normalized: dict[str, Any] = {
        "name": name,
        "type": "ip",
        "value": None,
        "members": [],
        "tags": [tag.get("name") for tag in tags if isinstance(tag, dict)],
    }

    if addr_type == "ipmask":
        subnet = address.get("subnet")
        if isinstance(subnet, str):
            try:
                ip, mask = subnet.split()
                normalized["value"] = str(ip_network(f"{ip}/{mask}", strict=False))
            except ValueError:
                normalized["value"] = subnet
    elif addr_type == "iprange":
        normalized["type"] = "range"
        normalized["value"] = f"{address.get('start-ip')}->{address.get('end-ip')}"
    elif addr_type == "fqdn":
        normalized["type"] = "fqdn"
        normalized["value"] = address.get("fqdn")
    elif addr_type == "group":
        normalized["type"] = "group"
        normalized["members"] = [member.get("name") for member in address.get("member", [])]
    else:
        normalized["value"] = address.get("subnet")

    if normalized["value"] is None and normalized["type"] != "group":
        normalized["value"] = address.get("subnet")

    return normalized


def _parse_service_ports(service: dict[str, Any]) -> list[dict[str, int]]:
    ports: list[dict[str, int]] = []
    portrange = service.get("tcp-portrange") or service.get("udp-portrange")
    if isinstance(portrange, str) and portrange:
        for part in portrange.split():
            if "-" in part:
                start, end = part.split("-", maxsplit=1)
            else:
                start = end = part
            try:
                ports.append({"start": int(start), "end": int(end)})
            except ValueError:
                continue
    return ports


def _normalize_service(service: dict[str, Any]) -> dict[str, Any]:
    proto = service.get("protocol") or service.get("protocol-number") or "tcp"
    return {
        "name": service.get("name"),
        "proto": proto,
        "ports": _parse_service_ports(service),
        "tags": service.get("tagging", []),
    }


def _normalize_policy(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "seq": policy.get("policyid"),
        "src_zones": [iface.get("name") for iface in policy.get("srcintf", [])],
        "dst_zones": [iface.get("name") for iface in policy.get("dstintf", [])],
        "src_addrs": [addr.get("name") for addr in policy.get("srcaddr", [])],
        "dst_addrs": [addr.get("name") for addr in policy.get("dstaddr", [])],
        "services": [svc.get("name") for svc in policy.get("service", [])],
        "action": policy.get("action"),
        "enabled": policy.get("status", "enable") == "enable",
        "log": policy.get("logtraffic", "all") != "disable",
        "schedule": policy.get("schedule"),
        "comments": policy.get("comments"),
        "nat": policy.get("nat") == "enable",
        "uuid": policy.get("uuid"),
    }


def normalize_fortigate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    addresses = [_normalize_address(addr) for addr in payload.get("addresses", [])]
    services = [_normalize_service(svc) for svc in payload.get("services", [])]
    policies = [_normalize_policy(pol) for pol in payload.get("policies", [])]

    return {
        "addresses": addresses,
        "services": services,
        "policies": policies,
        "metadata": payload.get("metadata", {}),
    }
