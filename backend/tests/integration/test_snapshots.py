from pathlib import Path


def _create_device(client, api_headers, tenant_id):
    payload = {
        "tenant_id": tenant_id,
        "vendor": "fortinet",
        "hostname": "edge-fw-01",
    }
    resp = client.post("/v1/devices", json=payload, headers=api_headers)
    return resp.json()["id"]


def test_upload_snapshot(client, api_headers, tenant_id, tmp_path):
    device_id = _create_device(client, api_headers, tenant_id)
    sample_path = Path(__file__).resolve().parents[1] / "fixtures" / "sample_fortigate.conf"

    with sample_path.open("rb") as handle:
        response = client.post(
            "/v1/snapshots:upload",
            headers=api_headers,
            data={"device_id": str(device_id)},
            files={"file": ("config.txt", handle, "text/plain")},
        )
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["normalized_json"]["policies"], "Policies should be parsed"
    assert payload["normalized_json"]["addresses"], "Addresses should be parsed"
