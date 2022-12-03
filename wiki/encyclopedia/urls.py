from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.entry, name='entry'),
    path('search', views.search, name='search'),
    path('new', views.new, name='new'),

]
handler404 = 'encyclopedia.views.page_not_found'