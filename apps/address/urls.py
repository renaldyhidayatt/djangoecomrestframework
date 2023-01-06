from django.urls import path
from .views import AddressListView

urlpatterns = [path("address", AddressListView.as_view(), name="address_list")]
