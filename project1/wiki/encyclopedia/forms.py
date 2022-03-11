from django import forms
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=True)
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        print("inside clean method")
        title = self.cleaned_data.get('title')
        exists = util.get_entry(title)
        if exists != None:
            self.add_error("title", "Entry with title '" + title + '" already exists!')
        return self.cleaned_data
