def test_summary_total_and_category_spend(client):
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
            "date": "2026-09-15",
        },
    )

    client.post(
        "/expenses",
        json={
            "amount": 300,
            "category": "Food",
            "note": "Dinner",
            "date": "2026-09-20",
        },
    )

    response = client.get(
        "/summary?month=2026-09-01"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_spend"] == 1800

    assert data["spend_by_category"]["Food"] == 800
    assert data["spend_by_category"]["Travel"] == 1000


def test_summary_month_over_month_change(client):
    # Previous month: ₹1,000
    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Food",
            "note": "August food",
            "date": "2026-08-10",
        },
    )

    # Current month: ₹1,500
    client.post(
        "/expenses",
        json={
            "amount": 1500,
            "category": "Food",
            "note": "September food",
            "date": "2026-09-10",
        },
    )

    response = client.get(
        "/summary?month=2026-09-01"
    )

    assert response.status_code == 200

    data = response.json()

    # (1500 - 1000) / 1000 * 100 = 50%
    assert data["month_over_month_change"] == 50.0


def test_summary_category_insight_over_20_percent(client):
    # Previous month: ₹1,000 Food
    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Food",
            "note": "August food",
            "date": "2026-08-10",
        },
    )

    # Current month: ₹1,300 Food
    client.post(
        "/expenses",
        json={
            "amount": 1300,
            "category": "Food",
            "note": "September food",
            "date": "2026-09-10",
        },
    )

    response = client.get(
        "/summary?month=2026-09-01"
    )

    assert response.status_code == 200

    data = response.json()

    insights = data["category_insights"]

    assert len(insights) == 1

    assert insights[0]["category"] == "Food"
    assert insights[0]["current_month_spend"] == 1300
    assert insights[0]["previous_month_spend"] == 1000
    assert insights[0]["increase_percentage"] == 30.0


def test_summary_without_previous_month_data(client):
    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "category": "Food",
            "note": "September food",
            "date": "2026-09-10",
        },
    )

    response = client.get(
        "/summary?month=2026-09-01"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_spend"] == 1000

    assert data["month_over_month_change"] is None

    assert data["category_insights"] == []