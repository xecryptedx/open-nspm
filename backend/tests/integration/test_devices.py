from app import models


def test_device_crud(client, api_headers, tenant_id):
    payload = {
        "tenant_id": tenant_id,
        "vendor": "fortinet",
        "hostname": "edge-fw-01",
        "mgmt_ip": "10.0.0.1",
        "api_url": "https://10.0.0.1",
        "metadata": {"model": "FG-100F"},
    }

    response = client.post("/v1/devices", json=payload, headers=api_headers)
    assert response.status_code == 201, response.text
    device_id = response.json()["id"]

    list_response = client.get("/v1/devices", headers=api_headers)
    assert list_response.status_code == 200
    assert any(device["id"] == device_id for device in list_response.json())

    get_response = client.get(f"/v1/devices/{device_id}", headers=api_headers)
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["hostname"] == "edge-fw-01"
