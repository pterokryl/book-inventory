import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0003_migrate_book_locations"),
    ]

    operations = [
        migrations.RemoveField(model_name="book", name="room"),
        migrations.RemoveField(model_name="book", name="cabinet"),
        migrations.RemoveField(model_name="book", name="shelf"),
        migrations.RenameField(model_name="book", old_name="location_shelf", new_name="shelf"),
        migrations.AlterField(
            model_name="book",
            name="shelf",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="books",
                to="books.shelf",
                verbose_name="Полка",
            ),
        ),
    ]
