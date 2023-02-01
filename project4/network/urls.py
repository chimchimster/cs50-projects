
from django.urls import path

from . import views

urlpatterns = [
    # Pages routes
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path("all-posts", views.all_posts, name="all-posts"),
    path("follows/<str:profile>", views.follows, name="follows"),

    # API routes
    path("profile/<str:profile>/subscribe", views.subscribe, name="subscribe"),
    path("profile/<str:profile>/unsubscribe", views.unsubscribe, name="unsubscribe"),
    path("posts", views.posts, name="posts"),

]
