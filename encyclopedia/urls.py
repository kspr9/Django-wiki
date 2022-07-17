from django.urls import path

from . import views

app_name="ency"

urlpatterns = [
    path("", views.index, name="index-page"),
    path("wiki/<str:entry_name>", views.entryview, name="entry"),
    path("search/", views.entry_search, name="search"),
    path("add_entry/", views.add_entry, name="add-entry"),
    path("wiki/<str:entry_name>/edit", views.edit_entry, name="edit-entry-path"),
    path("random", views.random_view, name="random"),
]
