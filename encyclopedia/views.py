from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

#import markdown as md
import markdown2 as md2
from markdown.extensions import Extension
from bs4 import BeautifulSoup as bs

#########################################################
###   Form classes        ###############################
#########################################################

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title")
    entry_content = forms.CharField(widget=forms.Textarea, label="Entry Content")

#########################################################
###   HELPER FUNCTIONS        ###########################
#########################################################

# this is a helper function to be used for extracting HTML from md file
def get_entry_html(entry_name):
    # accessing the md file contents
    entry = util.get_entry(entry_name)
    # generating html from md file
    html = md2.markdown(entry)

    return html

# this is a helper function for extracting the title of a md file
def get_entry_title(entry_name):
    # for separating title from all html
    soup = bs(get_entry_html(entry_name), 'html.parser')
    title = soup.find("h1").string

    return title

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
    
    # entry = util.get_entry(entry_name)
    html = get_entry_html(entry_name)
    title = get_entry_title(entry_name)

    return render(request, "encyclopedia/entry.html", {
            # "entry": entry,
            "entry_html": html,
            "title": title,
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

    #all_entries = util.list_entries()

    entries_found = [
        found_entry 
        for found_entry in util.list_entries()
        if search_term.lower() in found_entry.lower()]
    print(entries_found)

    return render(request, 'encyclopedia/search.html', {
        "search_term": search_term,
        "entries_found": entries_found,
    })

def add_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        # checks if the entered form data is valid, then proceeds to save the entry
        # otherwise redirects back to add_entry page
        if form.is_valid():
            # 'list arguments' refers to NewEntryForms variables
            entry_title = form.cleaned_data["entry_title"]
            entry_content = f'#{entry_title} \n{form.cleaned_data["entry_content"]}'
            
            # Display error message if entry already exsists
            if util.get_entry(entry_title):
                message = "The entry that you want to make already exists! Create a different one!"
                return render(request, "encyclopedia/add_entry.html", {
                "form": form,
                "message": message
            })

            # save the entry data to a file using util.save_entry function
            util.save_entry(entry_title, entry_content)

            # if a entry is added, redirect to back to home ie index page
            return entryview(request, entry_title)
        else:
            return render(request, "encyclopedia/add_entry.html", {
                "form": form
            })

    # by default redirects to add_entry page with NewEntryForm initialized
    return render(request, "encyclopedia/add_entry.html", {
        # give 'add_entry.html' template access to a variable called 'form' and 
        # link it to form builder class above
        "form": NewEntryForm()
        })