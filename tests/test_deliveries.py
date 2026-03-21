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
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_update_delivery(client):
    create_res = client.post(
        "/deliveries",
        json={"driver_name": "Update Me", "status": "created"},
    )

    delivery_id = create_res.json()["id"]

    update_res = client.put(
        f"/deliveries/{delivery_id}",
        json={"driver_name": "Updated", "status": "delivered"},
    )

    assert update_res.status_code == 200
    data = update_res.json()

    assert data["driver_name"] == "Updated"
    assert data["status"] == "delivered"