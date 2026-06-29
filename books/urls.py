from django.urls import path

from .views import (
    BookCreateView,
    BookListView,
    BookUpdateView,
    CabinetCreateView,
    CabinetOptionsView,
    CabinetUpdateView,
    LocationListView,
    RoomCreateView,
    RoomUpdateView,
    ShelfCreateView,
    ShelfOptionsView,
    ShelfUpdateView,
)

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="list"),
    path("create/", BookCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", BookUpdateView.as_view(), name="edit"),
    path("locations/", LocationListView.as_view(), name="locations"),
    path("locations/rooms/create/", RoomCreateView.as_view(), name="room_create"),
    path("locations/rooms/<int:pk>/edit/", RoomUpdateView.as_view(), name="room_edit"),
    path("locations/cabinets/create/", CabinetCreateView.as_view(), name="cabinet_create"),
    path("locations/cabinets/<int:pk>/edit/", CabinetUpdateView.as_view(), name="cabinet_edit"),
    path("locations/shelves/create/", ShelfCreateView.as_view(), name="shelf_create"),
    path("locations/shelves/<int:pk>/edit/", ShelfUpdateView.as_view(), name="shelf_edit"),
    path("api/cabinets/", CabinetOptionsView.as_view(), name="api_cabinets"),
    path("api/shelves/", ShelfOptionsView.as_view(), name="api_shelves"),
]
