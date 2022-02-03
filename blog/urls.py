from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/add/", views.PostCreateView.as_view(), name="post_add"),
    path("post/<int:pk>/update", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
