from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title=title) == None:
        return HttpResponseNotFound('<h1> 404 Error: page "' + title + '" not found')

    return render(request, "encyclopedia/entry.html", {
        "title": title
    })

