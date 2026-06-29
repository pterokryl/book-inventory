from django.contrib import admin

from .models import Book, Cabinet, Room, Shelf


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ("name", "room")
    list_filter = ("room",)
    search_fields = ("name", "room__name")


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ("name", "cabinet", "room_name")
    list_filter = ("cabinet__room", "cabinet")
    search_fields = ("name", "cabinet__name", "cabinet__room__name")

    @admin.display(description="Помещение")
    def room_name(self, obj):
        return obj.cabinet.room.name


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "publication_year", "room_name", "cabinet_name", "shelf")
    list_filter = ("publication_year", "shelf__cabinet__room", "shelf__cabinet")
    search_fields = ("author", "title", "shelf__name", "shelf__cabinet__name", "shelf__cabinet__room__name")

    @admin.display(description="Помещение")
    def room_name(self, obj):
        return obj.shelf.cabinet.room.name

    @admin.display(description="Шкаф")
    def cabinet_name(self, obj):
        return obj.shelf.cabinet.name
