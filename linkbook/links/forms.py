from django import forms
from taggit.forms import *

from linkbook.links.models import Link, Book


class BookForm(forms.Form):

    title = forms.CharField(
        widget = forms.TextInput(attrs = {'class': 'input-field'}),
        max_length = 30, required = True)
    description = forms.CharField(
        widget = forms.Textarea(attrs = {'class': 'materialize-textarea', 'id': 'description'}),
        max_length = 1000, required = False)


class LinkForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['books'].queryset = Book.objects.filter(user = user)
    
    url = forms.URLField(
        widget = forms.TextInput(attrs = {'class': ''}),
        max_length = 255)
    title = forms.CharField(
        widget = forms.TextInput(attrs = {'class': ''}),
        max_length = 30, required = True)
    description = forms.CharField(
        widget = forms.Textarea(attrs = {'class': 'materialize-textarea', 'id': 'description'}),
        max_length = 1000, required = False)
    tags = TagField()
    books = forms.ModelMultipleChoiceField(
        required = False,
        queryset = Book.objects.all(),
        widget = forms.widgets.CheckboxSelectMultiple())
    '''
    class Meta:
        model = Link
        fields = ['url', 'title', 'description', 'tags', 'books']
        widgets = {
            'description': forms.Textarea(),
            'books': forms.CheckboxSelectMultiple()
        }
    '''