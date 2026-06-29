from django import forms

from .models import Book, Cabinet, Room, Shelf


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "filter-input", "placeholder": "Например: Гостиная"})}


class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ["room", "name"]
        widgets = {
            "room": forms.Select(attrs={"class": "filter-input"}),
            "name": forms.TextInput(attrs={"class": "filter-input", "placeholder": "Например: Шкаф A"}),
        }


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ["cabinet", "name"]
        widgets = {
            "cabinet": forms.Select(attrs={"class": "filter-input"}),
            "name": forms.TextInput(attrs={"class": "filter-input", "placeholder": "Например: Полка 1"}),
        }

    def __init__(self, *args, room_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if room_id:
            self.fields["cabinet"].queryset = Cabinet.objects.filter(room_id=room_id).select_related("room")


class BookForm(forms.ModelForm):
    OTHER_VALUE = "__other__"

    author_choice = forms.ChoiceField(label="Автор", required=False)
    author_custom = forms.CharField(label="Новый автор", required=False)
    room = forms.ModelChoiceField(label="Помещение", queryset=Room.objects.all(), required=False)
    cabinet = forms.ModelChoiceField(label="Шкаф", queryset=Cabinet.objects.none(), required=False)
    shelf = forms.ModelChoiceField(label="Полка", queryset=Shelf.objects.none(), required=False)

    class Meta:
        model = Book
        fields = ["author", "title", "publication_year", "photo"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "filter-input"}),
            "publication_year": forms.NumberInput(attrs={"class": "filter-input"}),
            "photo": forms.ClearableFileInput(attrs={"class": "filter-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].required = False
        self.fields["author"].widget = forms.HiddenInput()

        self.fields["author_choice"].choices = self._build_author_choices()
        self.fields["author_custom"].widget.attrs.update(
            {"class": "filter-input", "placeholder": "Введите нового автора"}
        )

        for name in ("room", "cabinet", "shelf"):
            self.fields[name].widget.attrs["class"] = "filter-input"
            self.fields[name].empty_label = "Выберите значение"

        selected_room = None
        selected_cabinet = None

        if self.instance and self.instance.pk:
            selected_room = self.instance.shelf.cabinet.room_id
            selected_cabinet = self.instance.shelf.cabinet_id
            self.initial["room"] = selected_room
            self.initial["cabinet"] = selected_cabinet
            self.initial["shelf"] = self.instance.shelf_id
            self.initial["author_choice"] = self._initial_author_choice(self.instance.author)

        if self.data:
            selected_room = self.data.get("room") or selected_room
            selected_cabinet = self.data.get("cabinet") or selected_cabinet

        if selected_room:
            self.fields["cabinet"].queryset = Cabinet.objects.filter(room_id=selected_room)
        if selected_cabinet:
            self.fields["shelf"].queryset = Shelf.objects.filter(cabinet_id=selected_cabinet)

        self.fields["author_custom"].widget.attrs["style"] = "display:none;"

    @staticmethod
    def _distinct_authors():
        return Book.objects.values_list("author", flat=True).distinct().order_by("author")

    def _build_author_choices(self):
        return [
            ("", "Выберите значение"),
            *[(author, author) for author in self._distinct_authors()],
            (self.OTHER_VALUE, "Другое..."),
        ]

    def _initial_author_choice(self, value):
        authors = set(self._distinct_authors())
        return value if value in authors else self.OTHER_VALUE

    def clean(self):
        cleaned_data = super().clean()
        author_choice = cleaned_data.get("author_choice")
        author_custom = (cleaned_data.get("author_custom") or "").strip()

        if author_choice == self.OTHER_VALUE:
            cleaned_data["author"] = author_custom
        else:
            cleaned_data["author"] = (author_choice or "").strip()

        if not cleaned_data.get("author"):
            self.add_error("author_choice", "Укажите автора.")

        if not cleaned_data.get("room"):
            self.add_error("room", "Выберите помещение.")
        if not cleaned_data.get("cabinet"):
            self.add_error("cabinet", "Выберите шкаф.")
        if not cleaned_data.get("shelf"):
            self.add_error("shelf", "Выберите полку.")

        return cleaned_data

    def save(self, commit=True):
        self.instance.author = self.cleaned_data["author"]
        self.instance.shelf = self.cleaned_data["shelf"]
        return super().save(commit=commit)


class BookFilterForm(forms.Form):
    q = forms.CharField(label="Общий поиск", required=False)
    author = forms.CharField(label="Автор", required=False)
    title = forms.CharField(label="Название", required=False)
    publication_year = forms.IntegerField(label="Год издания", required=False)
    room = forms.ModelChoiceField(label="Помещение", queryset=Room.objects.all(), required=False)
    cabinet = forms.ModelChoiceField(label="Шкаф", queryset=Cabinet.objects.none(), required=False)
    shelf = forms.ModelChoiceField(label="Полка", queryset=Shelf.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "q": "Например: Оруэлл, 1984, Кабинет",
            "author": "ФИО автора",
            "title": "Название книги",
            "publication_year": "Например: 2020",
        }
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "filter-input"
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]
            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = "Все"

        selected_room = None
        selected_cabinet = None
        if self.data:
            selected_room = self.data.get("room") or None
            selected_cabinet = self.data.get("cabinet") or None

        if selected_room:
            self.fields["cabinet"].queryset = Cabinet.objects.filter(room_id=selected_room)
        else:
            self.fields["cabinet"].queryset = Cabinet.objects.all()

        if selected_cabinet:
            self.fields["shelf"].queryset = Shelf.objects.filter(cabinet_id=selected_cabinet)
        elif selected_room:
            self.fields["shelf"].queryset = Shelf.objects.filter(cabinet__room_id=selected_room)
        else:
            self.fields["shelf"].queryset = Shelf.objects.all()
