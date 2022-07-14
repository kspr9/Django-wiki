from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<slug:entry_name>", views.entryview, name="entry"),
]
