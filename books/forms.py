from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    OTHER_VALUE = "__other__"

    author_choice = forms.ChoiceField(label="Автор", required=False)
    author_custom = forms.CharField(label="Новый автор", required=False)
    room_choice = forms.ChoiceField(label="Помещение", required=False)
    room_custom = forms.CharField(label="Новое помещение", required=False)
    cabinet_choice = forms.ChoiceField(label="Шкаф", required=False)
    cabinet_custom = forms.CharField(label="Новый шкаф", required=False)
    shelf_choice = forms.ChoiceField(label="Полка", required=False)
    shelf_custom = forms.CharField(label="Новая полка", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].required = False
        self.fields["room"].required = False
        self.fields["cabinet"].required = False
        self.fields["shelf"].required = False

        self.fields["author"].widget = forms.HiddenInput()
        self.fields["room"].widget = forms.HiddenInput()
        self.fields["cabinet"].widget = forms.HiddenInput()
        self.fields["shelf"].widget = forms.HiddenInput()

        self.fields["author_choice"].choices = self._build_choices("author")
        self.fields["room_choice"].choices = self._build_choices("room")
        self.fields["cabinet_choice"].choices = self._build_choices("cabinet")
        self.fields["shelf_choice"].choices = self._build_choices("shelf")

        self.fields["author_custom"].widget.attrs["placeholder"] = "Введите нового автора"
        self.fields["room_custom"].widget.attrs["placeholder"] = "Введите новое помещение"
        self.fields["cabinet_custom"].widget.attrs["placeholder"] = "Введите новый шкаф"
        self.fields["shelf_custom"].widget.attrs["placeholder"] = "Введите новую полку"

        if self.instance and self.instance.pk:
            self.initial["author_choice"] = self._initial_choice("author", self.instance.author)
            self.initial["room_choice"] = self._initial_choice("room", self.instance.room)
            self.initial["cabinet_choice"] = self._initial_choice("cabinet", self.instance.cabinet)
            self.initial["shelf_choice"] = self._initial_choice("shelf", self.instance.shelf)

        for name, field in self.fields.items():
            field.widget.attrs["class"] = "filter-input"
            if name.endswith("_custom"):
                field.widget.attrs["data-custom-input"] = "true"
                field.widget.attrs["style"] = "display:none;"

    @staticmethod
    def _distinct_values(field_name):
        return (
            Book.objects.exclude(**{f"{field_name}__exact": ""})
            .values_list(field_name, flat=True)
            .distinct()
            .order_by(field_name)
        )

    def _build_choices(self, field_name):
        return [("", "Выберите значение"), *[(v, v) for v in self._distinct_values(field_name)], (self.OTHER_VALUE, "Другое...")]

    def _initial_choice(self, field_name, value):
        values = set(self._distinct_values(field_name))
        return value if value in values else self.OTHER_VALUE

    @staticmethod
    def _resolve_value(choice_value, custom_value):
        if choice_value == BookForm.OTHER_VALUE:
            return (custom_value or "").strip()
        return (choice_value or "").strip()

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["author"] = self._resolve_value(
            cleaned_data.get("author_choice"), cleaned_data.get("author_custom")
        )
        cleaned_data["room"] = self._resolve_value(
            cleaned_data.get("room_choice"), cleaned_data.get("room_custom")
        )
        cleaned_data["cabinet"] = self._resolve_value(
            cleaned_data.get("cabinet_choice"), cleaned_data.get("cabinet_custom")
        )
        cleaned_data["shelf"] = self._resolve_value(
            cleaned_data.get("shelf_choice"), cleaned_data.get("shelf_custom")
        )

        for field in ["author", "room", "cabinet", "shelf"]:
            if not cleaned_data.get(field):
                self.add_error(f"{field}_choice", "Поле обязательно: выберите значение или укажите новое.")
        return cleaned_data

    def save(self, commit=True):
        self.instance.author = self.cleaned_data["author"]
        self.instance.room = self.cleaned_data["room"]
        self.instance.cabinet = self.cleaned_data["cabinet"]
        self.instance.shelf = self.cleaned_data["shelf"]
        return super().save(commit=commit)

    class Meta:
        model = Book
        fields = [
            "author",
            "author_choice",
            "author_custom",
            "title",
            "publication_year",
            "room",
            "room_choice",
            "room_custom",
            "cabinet",
            "cabinet_choice",
            "cabinet_custom",
            "shelf",
            "shelf_choice",
            "shelf_custom",
            "photo",
        ]


class BookFilterForm(forms.Form):
    q = forms.CharField(label="Общий поиск", required=False)
    author = forms.CharField(label="Автор", required=False)
    title = forms.CharField(label="Название", required=False)
    publication_year = forms.IntegerField(label="Год издания", required=False)
    room = forms.CharField(label="Помещение", required=False)
    cabinet = forms.CharField(label="Шкаф", required=False)
    shelf = forms.CharField(label="Полка", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "q": "Например: Оруэлл, 1984, Кабинет",
            "author": "ФИО автора",
            "title": "Название книги",
            "publication_year": "Например: 2020",
            "room": "Например: Гостиная",
            "cabinet": "Например: Шкаф A",
            "shelf": "Например: Полка 1",
        }
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "placeholder": placeholders.get(name, ""),
                    "class": "filter-input",
                }
            )
