from django.template import RequestContext
from django.shortcuts import render
from django import forms
import markdown
from random import choice
from . import util

class InputForm(forms.Form):
    input_form = forms.CharField(label='', max_length=100)

class CreatePageForm(forms.Form):
    title = forms.CharField(label='Please add title', min_length=10, max_length=100)
    text_area = forms.CharField(label='Please add some text', widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}), min_length=50, max_length=5000)

class EditPageForm(forms.Form):
    title = forms.CharField(label='Change title', min_length=10, max_length=100)
    text_area = forms.CharField(label='Change text', widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}), min_length=50, max_length=5000)

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
        'content': html_file,
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
                        'title': data,
                        'content': content,
                        'form': form_instance,
                    })
                else:
                    return render(request, 'encyclopedia/index.html', {
                        'entries': substrings,
                        'form': form_instance,
                    })

def new(request):
    form = InputForm()
    if request.method == 'POST':
        form_page = CreatePageForm(request.POST)
        if form_page.is_valid():
            title = form_page.cleaned_data.get('title')
            text_area = form_page.cleaned_data.get('text_area')
            if title not in util.list_entries():
                util.save_entry(title, text_area)
                md_text = util.get_entry(title)
                html_text = markdown.markdown(md_text)
                return render(request, 'encyclopedia/entry.html', {
                    'title': title,
                    'form': form,
                    'content': html_text,
            })
            else:
                content = 'Page is Already Exists!'
                return render(request, 'encyclopedia/entry.html', {
                    'content': content,
                    'form': form,
                })
    else:
        form_page = CreatePageForm()
        return render(request, 'encyclopedia/new.html', {
            'form': form,
            'form_text': form_page
        })

def edit(request, title):
    form = InputForm()
    if request.method == 'POST':
        edit_form = EditPageForm(request.POST)
        if edit_form.is_valid():
            title_in = edit_form.cleaned_data.get('title')
            text = edit_form.cleaned_data.get('text_area')
            util.save_entry(title_in, text)
            html_text = markdown.markdown(text)
            return render(request, 'encyclopedia/entry.html', {
                'form': form,
                'title': title_in,
                'content': html_text,
                })
    elif request.method == 'GET':
        edit_form = EditPageForm({'title': title, 'text_area': util.get_entry(title)})
        return render(request, 'encyclopedia/edit.html', {
            'form': form,
            'title': title,
            'edit_form': edit_form,
            })
    return render(request, 'encyclopedia/404.html', {
            'form': form,
            'title': title,
            'content': 'Page is Already Exists!'
        })

def random_choice(request):
    form = InputForm()
    choosed = choice(util.list_entries())
    md_text = util.get_entry(choosed)
    html_text = markdown.markdown(md_text)
    return render(request, f'encyclopedia/entry.html', {
        'form': form,
        'title': choosed,
        'content': html_text,
    })
