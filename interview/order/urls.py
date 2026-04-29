from django.urls import path

from interview.order.views import (
    DeactivateOrderView,
    OrderEmbargoDateView,
    OrderListCreateView,
    OrderTagListCreateView,
    OrderTagsView,
    OrdersByTagView,
    OrdersFromJanToDateView,
)


urlpatterns = [
    path("tags/", OrderTagListCreateView.as_view(), name="order-tags-list"),
    path("tags/<int:id>/orders/", OrdersByTagView.as_view(), name="orders-by-tag"),
    path("embargo/", OrderEmbargoDateView.as_view(), name="order-embargo"),
    path("ytd/", OrdersFromJanToDateView.as_view(), name="orders-ytd"),
    path("<int:id>/tags/", OrderTagsView.as_view(), name="order-tags"),
    path("<int:id>/deactivate/", DeactivateOrderView.as_view(), name="order-deactivate"),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
