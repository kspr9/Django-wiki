from django.shortcuts import render

from . import util

#import markdown as md
import markdown2 as md2
from markdown.extensions import Extension
from bs4 import BeautifulSoup as bs


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def get_entry_html(entry_name):
    # accessing the md file contents
    entry = util.get_entry(entry_name)
    # generating html from md file
    html = md2.markdown(entry)

    return html

def get_entry_title(entry_name):
    # for separating title from all html
    soup = bs(get_entry_html(entry_name), 'html.parser')
    title = soup.find("h1").string
    
    return title

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