from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_index, name="post_index"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/create/", views.post_create, name="post_create"),
    path("post/<int:pk>/update/", views.post_update, name="post_update"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("user/<str:username>/", views.user_posts, name="user_posts"),
    path("post-likes/<int:pk>/", views.post_likes, name="post_likes"),
    path("post/<int:pk>/comment/", views.comment_create, name="comment_create")
]
