def register_user(client, email: str, password: str):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )


def login_user(client, email: str, password: str):
    return client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_create_delivery(client):
    register_user(client, "testcreate@example.com", "StrongPassword123!")
    login_response = login_user(client, "testcreate@example.com", "StrongPassword123!")
    token = login_response.json()["access_token"]

    response = client.post(
        "/deliveries",
        json={
            "driver_name": "Test Driver",
            "status": "in_transit",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201

    data = response.json()
    assert data["driver_name"] == "Test Driver"
    assert data["status"] == "in_transit"
    assert "id" in data
    assert "user_id" in data


def test_list_deliveries(client):
    register_user(client, "listuser@example.com", "StrongPassword123!")
    login_response = login_user(client, "listuser@example.com", "StrongPassword123!")
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/deliveries",
        json={"driver_name": "List Test", "status": "created"},
        headers=auth_headers(token),
    )
    assert create_response.status_code == 201

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
    register_user(client, "sortuser@example.com", "StrongPassword123!")
    login_response = login_user(client, "sortuser@example.com", "StrongPassword123!")
    token = login_response.json()["access_token"]

    response_one = client.post(
        "/deliveries",
        json={"driver_name": "Charlie", "status": "created"},
        headers=auth_headers(token),
    )
    response_two = client.post(
        "/deliveries",
        json={"driver_name": "Alice", "status": "created"},
        headers=auth_headers(token),
    )

    assert response_one.status_code == 201
    assert response_two.status_code == 201

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

def test_register_and_login_user(client):
    register_response = register_user(client, "user1@example.com", "StrongPassword123!")
    assert register_response.status_code == 201

    login_response = login_user(client, "user1@example.com", "StrongPassword123!")
    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_authenticated_user_can_create_delivery(client):
    register_user(client, "creator@example.com", "StrongPassword123!")
    login_response = login_user(client, "creator@example.com", "StrongPassword123!")

    token = login_response.json()["access_token"]

    response = client.post(
        "/deliveries",
        json={
            "driver_name": "Protected Driver",
            "status": "created",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["driver_name"] == "Protected Driver"
    assert data["status"] == "created"
    assert "user_id" in data


def test_owner_can_update_own_delivery(client):
    register_user(client, "owner@example.com", "StrongPassword123!")
    login_response = login_user(client, "owner@example.com", "StrongPassword123!")
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/deliveries",
        json={
            "driver_name": "Owner Driver",
            "status": "created",
        },
        headers=auth_headers(token),
    )
    delivery_id = create_response.json()["id"]

    update_response = client.put(
        f"/deliveries/{delivery_id}",
        json={
            "driver_name": "Updated Owner Driver",
            "status": "delivered",
        },
        headers=auth_headers(token),
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["driver_name"] == "Updated Owner Driver"
    assert data["status"] == "delivered"


def test_non_owner_cannot_update_delivery(client):
    register_user(client, "owner@example.com", "StrongPassword123!")
    owner_login = login_user(client, "owner@example.com", "StrongPassword123!")
    owner_token = owner_login.json()["access_token"]

    create_response = client.post(
        "/deliveries",
        json={
            "driver_name": "Owner Delivery",
            "status": "created",
        },
        headers=auth_headers(owner_token),
    )
    delivery_id = create_response.json()["id"]

    register_user(client, "other@example.com", "StrongPassword123!")
    other_login = login_user(client, "other@example.com", "StrongPassword123!")
    other_token = other_login.json()["access_token"]

    update_response = client.put(
        f"/deliveries/{delivery_id}",
        json={
            "driver_name": "Hacked Name",
            "status": "delivered",
        },
        headers=auth_headers(other_token),
    )

    assert update_response.status_code == 403
    assert update_response.json()["detail"] == "Not authorized to update this delivery"


def test_unauthenticated_user_cannot_create_delivery(client):
    response = client.post(
        "/deliveries",
        json={
            "driver_name": "No Auth Driver",
            "status": "created",
        },
    )

    assert response.status_code == 401