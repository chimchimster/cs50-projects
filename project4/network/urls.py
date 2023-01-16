
from django.urls import path

from . import views

urlpatterns = [
    # Pages routes
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path('all-posts', views.all_posts, name='all-posts'),

    # API routes
    path("profile/<str:profile>/subscribe", views.subscribe, name="subscribe"),
    path("profile/<str:profile>/unsubscribe", views.unsubscribe, name="unsubscribe"),
    path("profile/<str:profile>/followers", views.get_followers, name="followers"),
    path("posts", views.posts, name="posts"),
]
