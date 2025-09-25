from __future__ import annotations

from typing import Any


ANY_IDENTIFIERS = {"all", "ALL", "any"}


def _any_any_rules(policies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rule in policies:
        src = set(rule.get("src_addrs", []))
        dst = set(rule.get("dst_addrs", []))
        services = set(rule.get("services", []))
        if src & ANY_IDENTIFIERS and dst & ANY_IDENTIFIERS and services & ANY_IDENTIFIERS:
            findings.append(
                {
                    "type": "any_any",
                    "severity": "high",
                    "summary": f"Policy {rule.get('seq')} allows any-any",
                    "details": {"rule": rule},
                    "rule_ids": [rule.get("seq")],
                }
            )
    return findings


def _disabled_rules(policies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rule in policies:
        if not rule.get("enabled", True):
            findings.append(
                {
                    "type": "disabled_rule",
                    "severity": "low",
                    "summary": f"Policy {rule.get('seq')} is disabled",
                    "details": {"rule": rule},
                    "rule_ids": [rule.get("seq")],
                }
            )
    return findings


def _duplicates(_: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return []


def _shadowed(_: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return []


def _unused_objects(_: dict[str, Any]) -> list[dict[str, Any]]:
    return []


CHECK_HANDLERS = {
    "any_any": _any_any_rules,
    "disabled": _disabled_rules,
    "duplicates": _duplicates,
    "shadowed": _shadowed,
}


def run_hygiene(normalized: dict[str, Any], checks: list[str] | None = None) -> list[dict[str, Any]]:
    checks = checks or list(CHECK_HANDLERS.keys())
    policies = normalized.get("policies", [])
    findings: list[dict[str, Any]] = []
    for check in checks:
        handler = CHECK_HANDLERS.get(check)
        if handler:
            findings.extend(handler(policies))
        elif check == "unused_objects":
            findings.extend(_unused_objects(normalized))
    return findings
