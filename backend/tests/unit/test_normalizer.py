from pathlib import Path

from app.importers import fortigate_text
from app.services.normalizer import normalize_fortigate_payload


def test_normalizer_maps_addresses_and_policies():
    sample_path = Path(__file__).resolve().parents[1] / "fixtures" / "sample_fortigate.conf"
    raw = sample_path.read_text()
    parsed = fortigate_text.parse(raw)
    parsed["services"] = []

    normalized = normalize_fortigate_payload(parsed)

    assert normalized["addresses"][0]["name"] == "all"
    assert normalized["addresses"][0]["type"] == "ip"
    assert normalized["policies"][0]["seq"] == 1
    assert normalized["policies"][0]["src_addrs"] == ["all"]
