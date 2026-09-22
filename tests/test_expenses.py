def test_create_expense(client):
    response = client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "note": "Dinner",
            "date": "2026-09-22",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["amount"] == 500
    assert data["category"] == "Food"
    assert data["note"] == "Dinner"
    assert data["date"] == "2026-09-22"
    assert data["id"] == 1


def test_reject_negative_amount(client):
    response = client.post(
        "/expenses",
        json={
            "amount": -100,
            "category": "Food",
            "note": "Invalid",
            "date": "2026-09-22",
        },
    )

    assert response.status_code == 422


def test_reject_zero_amount(client):
    response = client.post(
        "/expenses",
        json={
            "amount": 0,
            "category": "Food",
            "note": "Invalid",
            "date": "2026-09-22",
        },
    )

    assert response.status_code == 422


def test_reject_empty_category(client):
    response = client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "",
            "note": "Invalid",
            "date": "2026-09-22",
        },
    )

    assert response.status_code == 422


def test_filter_expenses_by_category(client):
    client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "note": "Lunch",
            "date": "2026-09-20",
        },
    )

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Travel",
            "note": "Cab",
            "date": "2026-09-21",
        },
    )

    response = client.get("/expenses?category=Food")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Food"


def test_filter_expenses_by_date_range(client):
    client.post(
        "/expenses",
        json={
            "amount": 500,
            "category": "Food",
            "note": "Lunch",
            "date": "2026-09-10",
        },
    )

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Travel",
            "note": "Cab",
            "date": "2026-09-20",
        },
    )

    response = client.get(
        "/expenses"
        "?start_date=2026-09-15"
        "&end_date=2026-09-22"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Travel"


def test_reject_invalid_date_range(client):
    response = client.get(
        "/expenses"
        "?start_date=2026-09-22"
        "&end_date=2026-09-01"
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "start_date cannot be later than end_date"
    )