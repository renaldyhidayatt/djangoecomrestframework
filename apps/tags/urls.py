from django.urls import path
from .views import TagCreateListView

urlpatterns = [path("tags/", TagCreateListView.as_view(), name="tag_create_list")]
