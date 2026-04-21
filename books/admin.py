from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "publication_year", "room", "cabinet", "shelf")
    list_filter = ("publication_year", "room", "cabinet", "shelf")
    search_fields = ("author", "title", "room", "cabinet", "shelf")
