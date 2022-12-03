from django.template import RequestContext
from django.shortcuts import render
import markdown
from . import util

def page_not_found(request, exception):
    return render(request, 'encyclopedia/404.html', status=404)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_entry(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/404.html")
    md_text = util.get_entry(title)
    html_file = markdown.markdown(md_text)
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        'content': html_file
    })