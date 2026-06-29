from django.db import models


class Room(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="cabinets", verbose_name="Помещение")
    name = models.CharField("Название", max_length=120)

    class Meta:
        ordering = ["room__name", "name"]
        verbose_name = "Шкаф"
        verbose_name_plural = "Шкафы"
        constraints = [
            models.UniqueConstraint(fields=["room", "name"], name="unique_cabinet_per_room"),
        ]

    def __str__(self):
        return f"{self.room.name} — {self.name}"


class Shelf(models.Model):
    cabinet = models.ForeignKey(
        Cabinet, on_delete=models.CASCADE, related_name="shelves", verbose_name="Шкаф"
    )
    name = models.CharField("Название", max_length=120)

    class Meta:
        ordering = ["cabinet__room__name", "cabinet__name", "name"]
        verbose_name = "Полка"
        verbose_name_plural = "Полки"
        constraints = [
            models.UniqueConstraint(fields=["cabinet", "name"], name="unique_shelf_per_cabinet"),
        ]

    def __str__(self):
        return f"{self.cabinet.room.name} / {self.cabinet.name} / {self.name}"

    @property
    def room(self):
        return self.cabinet.room


class Book(models.Model):
    author = models.CharField("Автор", max_length=255)
    title = models.CharField("Название", max_length=255)
    publication_year = models.PositiveIntegerField("Год издания")
    shelf = models.ForeignKey(Shelf, on_delete=models.PROTECT, related_name="books", verbose_name="Полка")
    photo = models.ImageField("Фото", upload_to="book_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["author", "title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.author} — {self.title}"

    @property
    def room(self):
        return self.shelf.cabinet.room

    @property
    def cabinet(self):
        return self.shelf.cabinet
