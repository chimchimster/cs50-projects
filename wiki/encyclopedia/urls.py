from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.render_entry, name='render_entry'),

]
handler404 = 'encyclopedia.views.page_not_found'