from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

import markdown2 as md2
from bs4 import BeautifulSoup as bs

#########################################################
###   Form classes        ###############################
#########################################################

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(
        required=True,
        label="Title of the Entry: ",
    )
    entry_content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Content (markdown)",
                "id": "new_content",
            }
        ),
    )

class EditEntryForm(forms.Form):
    entry_content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "id": "new_content",
            }
        ),
    )

#########################################################
###   VIEWS        ######################################
#########################################################

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

# Detailed entry view
def entryview(request, entry_name):
    if not util.get_entry(entry_name):
        return render(request, "encyclopedia/notfound.html",)
    
    content = util.get_entry(entry_name)
    content_html = md2.markdown(content)
    
    return render(request, "encyclopedia/entry.html", {
            "entry_html": content_html,
            "title": entry_name,
    })

# Searching function
def entry_search(request):
    search_term = request.GET.get('q')

    # If the query matches the name of an encyclopedia entry, the user is redirected to that entry’s page.
    if search_term in util.list_entries():
        return entryview(request, search_term)
    
    # If the query does not match the name of an encyclopedia entry, 
    # the user is taken to a search results page that displays a list of all encyclopedia entries
    # that have the query as a substring.

    entries_found = [
        found_entry 
        for found_entry in util.list_entries()
        if search_term.lower() in found_entry.lower()
        ]

    return render(request, 'encyclopedia/search.html', {
        "search_term": search_term,
        "entries_found": entries_found,
    })

def add_entry(request):
    if request.method == "GET":
        # by default redirects to add_entry page with NewEntryForm initialized
        return render(request, "encyclopedia/add_entry.html", {
            # give 'add_entry.html' template access to a variable called 'form' and 
            # link it to form builder class above
            "form": NewEntryForm()
            })
    
    form = NewEntryForm(request.POST)
    if request.method == "POST" and form.is_valid():
        entry_title = form.cleaned_data.get("entry_title")
        entry_content = f'# {entry_title} \n {form.cleaned_data.get("entry_content")}'
        # Display error message if entry already exsists
        if util.get_entry(entry_title):
            message = "The entry that you want to make already exists! Create a different one!"
            return render(request, "encyclopedia/add_entry.html", {
            "form": form,
            "message": message,
            })

        # save the entry data to a file using util.save_entry function
        util.save_entry(entry_title, entry_content)

        # if a entry is added, redirect to back to home ie index page
        return redirect("ency:entry", entry_title)
    else:
        return render(request, "encyclopedia/add_entry.html", {
            "form": form
        })

def edit_entry(request, entry_name):
    if request.method == "GET":
        
        title = entry_name
        all_content = util.get_entry(entry_name)
        form = EditEntryForm({'entry_content': all_content})

        return render(request, "encyclopedia/edit_entry.html", {
            # give 'edit_entry.html' template access to a variable called 'title' and 'form' and 
            # link it to form builder class above
            "title": title,
            "form": form,
            })
    
    form = EditEntryForm(request.POST)
    # if the edited entry is saved ie method == "POST" then save entry and redirect to entry detail view
    if request.method == "POST" and form.is_valid():
        # reuse the same name for the entry >> no changing the name
        entry_title = entry_name
        # get the contents from EditEntryForm
        entry_content = form.cleaned_data.get("entry_content")
        # saving the entry with new data
        util.save_entry(entry_title, entry_content)
        # redirecting user back to entry detail page
        return redirect("ency:entry", entry_title)
    else:
        message = "Something went wrong with imputting data to entry change form. Try again"
        return render(request, "encyclopedia/edit_entry.html", {
            "form": form,
            "message": message
        })
        

    # defining the title to pass to html. Title should not be changed, or new entry will be created
    # displaying only contents without title in textarea
    
    
