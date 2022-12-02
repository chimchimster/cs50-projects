from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/css', views.render_css, name='css'),
    path('wiki/django', views.render_django, name='django'),
    path('wiki/git', views.render_git, name='git'),
    path('wiki/html', views.render_html, name='html'),
    path('wiki/python', views.render_python, name='python'),
]
handler404 = 'encyclopedia.views.page_not_found'