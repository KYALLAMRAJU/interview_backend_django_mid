from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    """Challenge 2: Set the is_active state on an order.

    PATCH /orders/<id>/deactivate/  -> sets is_active to False
    PATCH /orders/<id>/activate/    -> sets is_active to True
    """

    def patch(self, request: Request, *args, **kwargs) -> Response:
        try:
            order = Order.objects.get(id=kwargs["id"])
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=404)

        is_active = request.data.get("is_active")
        if is_active is None:
            return Response({"error": "Field 'is_active' is required."}, status=400)

        order.is_active = is_active
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=200)


class OrderEmbargoDateView(APIView):
    """Challenge 3: List orders between a start_date and embargo_date.

    Query params: ?start_date=YYYY-MM-DD&embargo_date=YYYY-MM-DD
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        start_date = request.query_params.get("start_date")
        embargo_date = request.query_params.get("embargo_date")

        if not start_date or not embargo_date:
            return Response(
                {"error": "Query parameters 'start_date' and 'embargo_date' are required."},
                status=400,
            )

        queryset = self.queryset.filter(
            start_date__gte=start_date,
            embargo_date__lte=embargo_date,
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=200)


class OrderTagsView(APIView):
    """Challenge 6: List all tags associated with an order."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            order = Order.objects.get(id=kwargs["id"])
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=404)

        serializer = OrderTagSerializer(order.tags.all(), many=True)
        return Response(serializer.data, status=200)


class OrdersByTagView(APIView):
    """Challenge 7: List all orders associated with a particular tag."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            tag = OrderTag.objects.get(id=kwargs["id"])
        except OrderTag.DoesNotExist:
            return Response({"error": "Tag not found."}, status=404)

        serializer = OrderSerializer(tag.orders.all(), many=True)
        return Response(serializer.data, status=200)


