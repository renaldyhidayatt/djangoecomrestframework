from django.urls import path
from apps.product.views import ProductListView, ProductDetailsView

urlpatterns = [
    path("products", ProductListView.as_view(), name="product_list"),
    path(
        "products/<slug:string>", ProductDetailsView.as_view(), name="product_details"
    ),
    path(
        "products/by_id/<pk>",
        ProductDetailsView.as_view(),
        name="product_details_by_id",
    ),
]
