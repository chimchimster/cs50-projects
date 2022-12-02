from django.template import RequestContext
from django.shortcuts import render

from . import util

def page_not_found(request, exception):
    return render(request, 'encyclopedia/404.html', status=404)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_css(request):
    return render(request, 'encyclopedia/CSS.html')

def render_django(request):
    return render(request, 'encyclopedia/Django.html')

def render_git(request):
    return render(request, 'encyclopedia/Git.html')

def render_python(request):
    return render(request, 'encyclopedia/Python.html')

def render_html(request):
    return render(request, 'encyclopedia/HTML.html')