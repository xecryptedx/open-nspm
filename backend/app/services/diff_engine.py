from __future__ import annotations

from typing import Any


def _rule_key(rule: dict[str, Any]) -> str:
    return rule.get("uuid") or f"seq:{rule.get('seq')}"


def diff_policies(base: list[dict[str, Any]], head: list[dict[str, Any]]) -> dict[str, Any]:
    base_map = {_rule_key(rule): rule for rule in base}
    head_map = {_rule_key(rule): rule for rule in head}

    added_keys = set(head_map) - set(base_map)
    removed_keys = set(base_map) - set(head_map)
    common_keys = set(base_map) & set(head_map)

    modified: list[dict[str, Any]] = []
    for key in common_keys:
        base_rule = base_map[key]
        head_rule = head_map[key]
        if base_rule != head_rule:
            changes: dict[str, tuple[Any, Any]] = {}
            for field in sorted(set(base_rule) | set(head_rule)):
                if base_rule.get(field) != head_rule.get(field):
                    changes[field] = (base_rule.get(field), head_rule.get(field))
            modified.append({"key": key, "changes": changes})

    return {
        "summary": {
            "added": len(added_keys),
            "removed": len(removed_keys),
            "modified": len(modified),
        },
        "details": {
            "added": [head_map[key] for key in sorted(added_keys)],
            "removed": [base_map[key] for key in sorted(removed_keys)],
            "modified": modified,
        },
    }


def compute_diff(base_snapshot: dict[str, Any], head_snapshot: dict[str, Any]) -> dict[str, Any]:
    base_policies = base_snapshot.get("policies", [])
    head_policies = head_snapshot.get("policies", [])
    policy_diff = diff_policies(base_policies, head_policies)
    return {
        "summary": {"policies": policy_diff["summary"]},
        "details": {"policies": policy_diff["details"]},
    }
