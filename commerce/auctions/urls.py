from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.unique_listing, name='listing'),
    path('create', views.create_listing, name='create'),
    path('remove/<int:listing_id>', views.remove_from_watchlist, name='remove_wl'),
    path('add_wl/<int:listing_id>', views.add_to_watchlist, name='add_wl'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('bid/<int:listing_id>', views.bid, name='bid'),
    path('close/<int:listing_id>', views.close_bid, name='close'),
    path('categories', views.categories, name='categories'),
    path('categories/<str:category>', views.unique_category, name='category'),
    path('comments/<int:listing_id>', views.comment, name='comments'),

]
