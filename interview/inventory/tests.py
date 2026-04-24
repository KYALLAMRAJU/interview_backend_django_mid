import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType


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
def inventory_tag(db):
    return InventoryTag.objects.create(name="Action")


@pytest.fixture
def inventory(db, inventory_type, inventory_language, inventory_tag):
    item = Inventory.objects.create(
        name="The Matrix",
        type=inventory_type,
        language=inventory_language,
        metadata={"year": 1999, "actors": ["Keanu Reeves"], "imdb_rating": 8.7, "rotten_tomatoes_rating": 87, "film_locations": []},
    )
    item.tags.add(inventory_tag)
    return item


# --- Challenge 1: Inventory Dates ---

@pytest.mark.django_db
def test_inventory_created_after_returns_results(api_client, inventory):
    url = "/inventory/created-after/"
    response = api_client.get(url, {"date": "2000-01-01"})
    assert response.status_code == 200
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_inventory_created_after_future_date_returns_empty(api_client, inventory):
    url = "/inventory/created-after/"
    response = api_client.get(url, {"date": "2099-01-01"})
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_inventory_created_after_missing_date_returns_400(api_client, inventory):
    url = "/inventory/created-after/"
    response = api_client.get(url)
    assert response.status_code == 400
    assert "error" in response.data


# --- Challenge 5: Inventory Pagination ---

@pytest.fixture
def many_inventory_items(db, inventory_type, inventory_language):
    items = []
    for i in range(7):
        item = Inventory.objects.create(
            name=f"Movie {i}",
            type=inventory_type,
            language=inventory_language,
            metadata={"year": 2000 + i, "actors": [], "imdb_rating": 7.0, "rotten_tomatoes_rating": 70, "film_locations": []},
        )
        items.append(item)
    return items


@pytest.mark.django_db
def test_inventory_list_defaults_to_3_items(api_client, many_inventory_items):
    response = api_client.get("/inventory/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 3
    assert response.data["limit"] == 3
    assert response.data["offset"] == 0


@pytest.mark.django_db
def test_inventory_list_pagination_offset(api_client, many_inventory_items):
    response = api_client.get("/inventory/", {"offset": 3, "limit": 3})
    assert response.status_code == 200
    assert len(response.data["results"]) == 3
    assert response.data["offset"] == 3


@pytest.mark.django_db
def test_inventory_list_pagination_count(api_client, many_inventory_items):
    response = api_client.get("/inventory/")
    assert response.status_code == 200
    assert response.data["count"] == 7


@pytest.mark.django_db
def test_inventory_list_custom_limit(api_client, many_inventory_items):
    response = api_client.get("/inventory/", {"limit": 5})
    assert response.status_code == 200
    assert len(response.data["results"]) == 5

