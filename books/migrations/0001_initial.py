from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("author", models.CharField(max_length=255, verbose_name="Автор")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("publication_year", models.PositiveIntegerField(verbose_name="Год издания")),
                ("room", models.CharField(max_length=120, verbose_name="Помещение")),
                ("cabinet", models.CharField(max_length=120, verbose_name="Шкаф")),
                ("shelf", models.CharField(max_length=120, verbose_name="Полка")),
                ("photo", models.ImageField(blank=True, null=True, upload_to="book_photos/", verbose_name="Фото")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Книга",
                "verbose_name_plural": "Книги",
                "ordering": ["author", "title"],
            },
        ),
    ]
