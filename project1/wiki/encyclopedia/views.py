from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
import markdown2

from . import util
from .forms import NewEntryForm


def index(request):
    query = request.GET.get('q')
    entries = util.list_entries()

    # if no q then show all
    if query == None:
        return render(request, "encyclopedia/index.html", {
            "title": "All Pages",
            "entries": entries
        })

    # if q matches one entry exactly then redirect to that entry
    match = util.get_entry(query)
    if match != None:
        return redirect('entry', title=query)

    # show all entries that match on substr
    filtered_entries = []
    for entry in entries:
        if query in entry:
            filtered_entries.append(entry)

    return render(request, "encyclopedia/index.html", {
                "title": 'Search results for "' + query + '"',
                "entries": filtered_entries
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

def create(request):
    if request.method == 'POST':
        print("form submitted")
        form = NewEntryForm(request.POST)

        if form.is_valid():
            print("form is valid")
        else:
            print(form.errors)
            return render(request, "encyclopedia/create.html", {'form': form})

    

    form = NewEntryForm()
    return render(request, "encyclopedia/create.html", {'form': form})

