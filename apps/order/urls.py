from django.urls import path
from apps.order.views import OrderListView, OrderDetailsView

urlpatterns = [
    path("orders", OrderListView.as_view(), name="order_list"),
    path("order/<pk>", OrderDetailsView.as_view(), name="order_details"),
]
