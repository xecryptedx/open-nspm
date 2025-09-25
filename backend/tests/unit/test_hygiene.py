from app.services.hygiene import run_hygiene


def test_any_any_detection_flags_rule():
    normalized = {
        "policies": [
            {
                "seq": 1,
                "src_addrs": ["all"],
                "dst_addrs": ["all"],
                "services": ["ALL"],
                "enabled": True,
            }
        ]
    }

    findings = run_hygiene(normalized, checks=["any_any"])
    assert findings
    assert findings[0]["type"] == "any_any"
