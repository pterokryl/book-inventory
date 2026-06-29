from django.db import migrations


def migrate_book_locations(apps, schema_editor):
    Book = apps.get_model("books", "Book")
    Room = apps.get_model("books", "Room")
    Cabinet = apps.get_model("books", "Cabinet")
    Shelf = apps.get_model("books", "Shelf")

    for book in Book.objects.all():
        room, _ = Room.objects.get_or_create(name=book.room)
        cabinet, _ = Cabinet.objects.get_or_create(room=room, name=book.cabinet)
        shelf, _ = Shelf.objects.get_or_create(cabinet=cabinet, name=book.shelf)
        book.location_shelf = shelf
        book.save(update_fields=["location_shelf"])


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_location_hierarchy"),
    ]

    operations = [
        migrations.RunPython(migrate_book_locations, migrations.RunPython.noop),
    ]
