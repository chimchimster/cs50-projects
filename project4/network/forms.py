from django import forms


class PostFrom(forms.Form):
    text_area = forms.CharField(widget=forms.Textarea)

