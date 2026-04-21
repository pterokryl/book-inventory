from django.db import models


class Book(models.Model):
    author = models.CharField("Автор", max_length=255)
    title = models.CharField("Название", max_length=255)
    publication_year = models.PositiveIntegerField("Год издания")
    room = models.CharField("Помещение", max_length=120)
    cabinet = models.CharField("Шкаф", max_length=120)
    shelf = models.CharField("Полка", max_length=120)
    photo = models.ImageField("Фото", upload_to="book_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["author", "title"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"{self.author} — {self.title}"
