from django.urls import path
from .views import CommentListView, CommentsDetailsView

urlpatterns = [
    path(
        "products/<slug:string>/comments",
        CommentListView.as_view(),
        name="comment_list",
    ),
    path("comments/<pk>", CommentsDetailsView.as_view(), name="comment_details_short"),
    path(
        "products/<slug:string>/comments/<pk>",
        CommentsDetailsView.as_view(),
        name="comment_details",
    ),
]
