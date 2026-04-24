# Challenge 8 — How to Add an Inventory Item Through the API

Hey! Let me walk you through exactly how to solve this. By the end you'll have working code.

---

## What you're trying to do

You want to send a POST request to `/inventory/` and create an inventory item. The `metadata` field must include:
- `year`
- `actors`
- `imdb_rating`
- `rotten_tomatoes_rating`
- `film_locations`

---

## Step 1 — Update the schema to include `film_locations`

The metadata is validated by a Pydantic schema in `interview/inventory/schemas.py`. Right now it doesn't have `film_locations`. Add it:

```python
# interview/inventory/schemas.py
from decimal import Decimal
from pydantic import BaseModel


class InventoryMetaData(BaseModel):
    year: int
    actors: list[str]
    imdb_rating: Decimal
    rotten_tomatoes_rating: int
    film_locations: list[str]  # <-- add this
```

---

## Step 2 — Make sure the serializer can write nested fields

The `InventorySerializer` in `interview/inventory/serializers.py` uses nested read-only serializers for `type` and `language`. To create via the API, you need to accept IDs instead. Update the serializer:

```python
# interview/inventory/serializers.py
from rest_framework import serializers
from interview.inventory.models import Inventory, InventoryLanguage, InventoryTag, InventoryType


class InventoryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTag
        fields = ["id", "name", "is_active"]


class InventoryLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLanguage
        fields = ["id", "name"]


class InventoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryType
        fields = ["id", "name"]


class InventorySerializer(serializers.ModelSerializer):
    type = InventoryTypeSerializer(read_only=True)
    language = InventoryLanguageSerializer(read_only=True)
    tags = InventoryTagSerializer(many=True, read_only=True)
    metadata = serializers.JSONField()
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryType.objects.all(), source="type", write_only=True
    )
    language_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryLanguage.objects.all(), source="language", write_only=True
    )

    class Meta:
        model = Inventory
        fields = ["id", "name", "type", "type_id", "language", "language_id", "tags", "metadata"]
```

---

## Step 3 — Send the POST request

Use any HTTP client (curl, Postman, or the DRF browser). Here's the JSON body:

```json
{
    "name": "Inception",
    "type_id": 1,
    "language_id": 37,
    "metadata": {
        "year": 2010,
        "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
        "imdb_rating": 8.8,
        "rotten_tomatoes_rating": 87,
        "film_locations": ["London", "Paris", "Tokyo"]
    }
}
```

**Endpoint:**
```
POST http://127.0.0.1:8002/inventory/
Content-Type: application/json
```

---

## Step 4 — What to check if it doesn't work

| Problem | Fix |
|---|---|
| `metadata` validation error | Make sure all 5 fields are present in `metadata` |
| `type_id` / `language_id` invalid | Check valid IDs at `GET /inventory/types/` and `GET /inventory/languages/` |
| 400 on serializer | Check `serializer.errors` in the response body |

---

## How it flows internally

1. `POST /inventory/` hits `InventoryListCreateView.post()`
2. `InventoryMetaData(**request.data["metadata"])` validates the metadata via Pydantic — this is where `film_locations` must be present
3. The validated metadata dict is passed to the serializer
4. The serializer validates `type_id`, `language_id`, and `name`
5. `serializer.save()` creates the `Inventory` record in the database

That's it — you should get a `201 Created` response with the full inventory object!

