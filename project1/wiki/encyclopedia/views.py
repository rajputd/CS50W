from django.shortcuts import render
from django.http import HttpResponseNotFound
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    raw_content = util.get_entry(title=title)
    if raw_content == None:
        return HttpResponseNotFound('<h1> 404 Error: page "' + title + '" not found')

    content = markdown2.markdown(raw_content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

