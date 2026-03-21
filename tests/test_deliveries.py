def test_create_delivery(client):
    response = client.post(
        "/deliveries",
        json={
            "driver_name": "Test Driver",
            "status": "in_transit",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["driver_name"] == "Test Driver"
    assert data["status"] == "in_transit"
    assert "id" in data


def test_list_deliveries(client):
    client.post(
        "/deliveries",
        json={"driver_name": "List Test", "status": "created"},
    )

    response = client.get("/deliveries")

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert isinstance(data["items"], list)
    assert data["total"] >= 1


def test_list_deliveries_sorted_by_driver_name(client):
    client.post(
        "/deliveries",
        json={"driver_name": "Charlie", "status": "created"},
    )
    client.post(
        "/deliveries",
        json={"driver_name": "Alice", "status": "created"},
    )

    response = client.get(
        "/deliveries",
        params={"sort_by": "driver_name", "sort_order": "asc"},
    )

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    names = [item["driver_name"] for item in data["items"]]
    assert "Alice" in names
    assert "Charlie" in names