from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryTag,
    InventoryType,
)
from interview.inventory.schemas import InventoryMetaData
from interview.inventory.serializers import (
    InventoryLanguageSerializer,
    InventorySerializer,
    InventoryTagSerializer,
    InventoryTypeSerializer,
)


class InventoryListCreateView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            metadata = InventoryMetaData(**request.data["metadata"])
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        request.data["metadata"] = metadata.dict()
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        limit = int(request.query_params.get("limit", 3))
        offset = int(request.query_params.get("offset", 0))
        queryset = self.get_queryset()
        total = queryset.count()
        page = queryset[offset: offset + limit]
        serializer = self.serializer_class(page, many=True)
        return Response(
            {
                "count": total,
                "limit": limit,
                "offset": offset,
                "results": serializer.data,
            },
            status=200,
        )

    def get_queryset(self):
        return self.queryset.all()


class InventoryRetrieveUpdateDestroyView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTagListCreateView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryTagRetrieveUpdateDestroyView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory_tag)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(
            inventory_tag, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        inventory_tag.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryLanguageListCreateView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryLanguageRetrieveUpdateDestroyView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTypeListCreateView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryTypeRetrieveUpdateDestroyView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryCreatedAfterView(APIView):
    """Challenge 1: List inventory items created after a certain day.

    Query param: ?date=YYYY-MM-DD
    """

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        date = request.query_params.get("date")
        if not date:
            return Response({"error": "Query parameter 'date' is required."}, status=400)

        queryset = self.queryset.filter(created_at__date__gt=date)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=200)


