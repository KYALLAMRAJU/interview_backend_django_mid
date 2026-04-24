import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from interview.order.models import Order, OrderTag


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def inventory_type(db):
    return InventoryType.objects.create(name="Movie")


@pytest.fixture
def inventory_language(db):
    return InventoryLanguage.objects.create(name="English")


@pytest.fixture
def inventory(db, inventory_type, inventory_language):
    return Inventory.objects.create(
        name="The Matrix",
        type=inventory_type,
        language=inventory_language,
        metadata={"year": 1999, "actors": [], "imdb_rating": 8.7, "rotten_tomatoes_rating": 87, "film_locations": []},
    )


@pytest.fixture
def order_tag(db):
    return OrderTag.objects.create(name="Pending")


@pytest.fixture
def order(db, inventory, order_tag):
    today = date.today()
    o = Order.objects.create(
        inventory=inventory,
        start_date=today,
        embargo_date=today + timedelta(days=30),
    )
    o.tags.add(order_tag)
    return o


# --- Challenge 2: Deactivate Order ---

@pytest.mark.django_db
def test_deactivate_order(api_client, order):
    assert order.is_active is True
    response = api_client.patch(f"/orders/{order.id}/deactivate/", {"is_active": False}, format="json")
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.is_active is False


@pytest.mark.django_db
def test_activate_order(api_client, order):
    order.is_active = False
    order.save()
    response = api_client.patch(f"/orders/{order.id}/deactivate/", {"is_active": True}, format="json")
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.is_active is True


@pytest.mark.django_db
def test_deactivate_order_not_found(api_client):
    response = api_client.patch("/orders/9999/deactivate/", {"is_active": False}, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_deactivate_order_missing_field(api_client, order):
    response = api_client.patch(f"/orders/{order.id}/deactivate/", {}, format="json")
    assert response.status_code == 400


# --- Challenge 3: Embargo Date ---

@pytest.mark.django_db
def test_embargo_date_returns_matching_orders(api_client, order):
    today = date.today()
    response = api_client.get("/orders/embargo/", {
        "start_date": str(today),
        "embargo_date": str(today + timedelta(days=30)),
    })
    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_embargo_date_no_match(api_client, order):
    response = api_client.get("/orders/embargo/", {
        "start_date": "2000-01-01",
        "embargo_date": "2000-01-31",
    })
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_embargo_date_missing_params(api_client):
    response = api_client.get("/orders/embargo/")
    assert response.status_code == 400
    assert "error" in response.data


# --- Challenge 6: Tags on Orders ---

@pytest.mark.django_db
def test_order_tags_returns_tags(api_client, order, order_tag):
    response = api_client.get(f"/orders/{order.id}/tags/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == order_tag.name


@pytest.mark.django_db
def test_order_tags_not_found(api_client):
    response = api_client.get("/orders/9999/tags/")
    assert response.status_code == 404


# --- Challenge 7: Orders on Tag ---

@pytest.mark.django_db
def test_orders_by_tag_returns_orders(api_client, order, order_tag):
    response = api_client.get(f"/orders/tags/{order_tag.id}/orders/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_orders_by_tag_not_found(api_client):
    response = api_client.get("/orders/tags/9999/orders/")
    assert response.status_code == 404

