from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
import markdown2

from . import util
from .forms import EditEntryForm, NewEntryForm


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
        print("create entry form submitted")
        form = NewEntryForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            #check if already exists
            exists = util.get_entry(cleaned_data["title"])
            if exists != None:
                print("Rejected entry submission: Entry with title '" + cleaned_data["title"] + '" already exists!')
                form.add_error("title", "Entry with title '" + cleaned_data["title"] + '" already exists!')
                return render(request, "encyclopedia/create.html", {'form': form})

            print("saving new entry...")
            util.save_entry(cleaned_data['title'], cleaned_data['content'])
            return redirect('entry', title=cleaned_data['title'])
        else:
            print("Rejected entry submission for some generic reason")
            return render(request, "encyclopedia/create.html", {'form': form})

    # render a empty form
    form = NewEntryForm()
    return render(request, "encyclopedia/create.html", {'form': form})

def edit(request, title):
    if request.method == 'POST':
        print("edit entry form submitted")
        form = EditEntryForm(request.POST)

        if form.is_valid():
            print("saving entry edits...")
            util.save_entry(title, form.cleaned_data['content'])
            return redirect('entry', title=title)
        else:
            print("Rejected entry edit submission for some generic reason")
            return render(request, "encyclopedia/edit.html", {'form': form})

    #render prefilled form
    content = util.get_entry(title)
    form = EditEntryForm({ 'content': content })
    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'form': form
    })

