from django.template import RequestContext
from django.shortcuts import render
from django import forms
import markdown
from . import util

class InputForm(forms.Form):
    input_form = forms.CharField(label='', max_length=100)

def page_not_found(request, exception):
    return render(request, 'encyclopedia/404.html', status=404)

def index(request):
    form = InputForm
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': form
    })

def entry(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/404.html")
    md_text = util.get_entry(title)
    html_file = markdown.markdown(md_text)
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        'content': html_file
    })

def search(request):
    if request.method == 'POST':
        form_instance = InputForm(request.POST)
        if form_instance.is_valid():
            data = form_instance.cleaned_data.get('input_form')
            if data in util.list_entries():
                md_text = util.get_entry(data)
                html_text = markdown.markdown(md_text)
                return render(request, 'encyclopedia/entry.html', {
                    'content': html_text,
                    'title': data
                })
            else:
                substrings = list(filter(lambda x: data in x.lower(), util.list_entries()))
                if not substrings:
                    content = 'Requested Page is not Found on Server'
                    return render(request, 'encyclopedia/404.html', {
                        'content': content,
                    })
                else:
                    return render(request, 'encyclopedia/index.html', {
                        'entries': substrings,
                    })



