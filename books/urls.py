from django.urls import path

from .views import BookCreateView, BookListView, BookUpdateView

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="list"),
    path("create/", BookCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", BookUpdateView.as_view(), name="edit"),
]
