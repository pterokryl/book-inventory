import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Помещение",
                "verbose_name_plural": "Помещения",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Cabinet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cabinets",
                        to="books.room",
                        verbose_name="Помещение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Шкаф",
                "verbose_name_plural": "Шкафы",
                "ordering": ["room__name", "name"],
            },
        ),
        migrations.CreateModel(
            name="Shelf",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                (
                    "cabinet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shelves",
                        to="books.cabinet",
                        verbose_name="Шкаф",
                    ),
                ),
            ],
            options={
                "verbose_name": "Полка",
                "verbose_name_plural": "Полки",
                "ordering": ["cabinet__room__name", "cabinet__name", "name"],
            },
        ),
        migrations.AddConstraint(
            model_name="cabinet",
            constraint=models.UniqueConstraint(fields=("room", "name"), name="unique_cabinet_per_room"),
        ),
        migrations.AddConstraint(
            model_name="shelf",
            constraint=models.UniqueConstraint(fields=("cabinet", "name"), name="unique_shelf_per_cabinet"),
        ),
        migrations.AddField(
            model_name="book",
            name="location_shelf",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="books",
                to="books.shelf",
                verbose_name="Полка",
            ),
        ),
    ]
