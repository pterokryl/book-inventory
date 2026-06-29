from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .forms import BookFilterForm, BookForm, CabinetForm, RoomForm, ShelfForm
from .models import Book, Cabinet, Room, Shelf


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 25

    def get_queryset(self):
        qs = Book.objects.select_related("shelf__cabinet__room")
        self.filter_form = BookFilterForm(self.request.GET or None)

        if self.filter_form.is_valid():
            q = self.filter_form.cleaned_data.get("q")
            author = self.filter_form.cleaned_data.get("author")
            title = self.filter_form.cleaned_data.get("title")
            publication_year = self.filter_form.cleaned_data.get("publication_year")
            room = self.filter_form.cleaned_data.get("room")
            cabinet = self.filter_form.cleaned_data.get("cabinet")
            shelf = self.filter_form.cleaned_data.get("shelf")

            if q:
                query = (
                    Q(author__icontains=q)
                    | Q(title__icontains=q)
                    | Q(shelf__name__icontains=q)
                    | Q(shelf__cabinet__name__icontains=q)
                    | Q(shelf__cabinet__room__name__icontains=q)
                )
                if q.isdigit():
                    query |= Q(publication_year=int(q))
                qs = qs.filter(query)
            if author:
                qs = qs.filter(author__icontains=author)
            if title:
                qs = qs.filter(title__icontains=title)
            if publication_year:
                qs = qs.filter(publication_year=publication_year)
            if room:
                qs = qs.filter(shelf__cabinet__room=room)
            if cabinet:
                qs = qs.filter(shelf__cabinet=cabinet)
            if shelf:
                qs = qs.filter(shelf=shelf)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", BookFilterForm())
        params = self.request.GET.copy()
        params.pop("page", None)
        context["query_params"] = params.urlencode()
        context["has_active_filters"] = any(
            value not in (None, "")
            for key, value in self.request.GET.items()
            if key != "page"
        )
        return context


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:list")


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:list")


class LocationListView(TemplateView):
    template_name = "books/location_list.html"

    def get_context_data(self, **kwargs):
        from django.db.models import Count, Prefetch

        context = super().get_context_data(**kwargs)
        cabinets_qs = Cabinet.objects.annotate(
            shelf_count=Count("shelves", distinct=True),
            book_count=Count("shelves__books", distinct=True),
        ).order_by("name")
        context["rooms"] = (
            Room.objects.prefetch_related(
                Prefetch("cabinets", queryset=cabinets_qs.prefetch_related("shelves"))
            )
            .annotate(cabinet_count=Count("cabinets", distinct=True))
            .order_by("name")
        )
        context["stats"] = {
            "rooms": Room.objects.count(),
            "cabinets": Cabinet.objects.count(),
            "shelves": Shelf.objects.count(),
        }
        return context


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = "books/location_form.html"
    success_url = reverse_lazy("books:locations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новое помещение"
        return context


class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "books/location_form.html"
    success_url = reverse_lazy("books:locations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование помещения"
        return context


class CabinetCreateView(CreateView):
    model = Cabinet
    form_class = CabinetForm
    template_name = "books/location_form.html"
    success_url = reverse_lazy("books:locations")

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get("room")
        if room_id:
            initial["room"] = room_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новый шкаф"
        return context


class CabinetUpdateView(UpdateView):
    model = Cabinet
    form_class = CabinetForm
    template_name = "books/location_form.html"
    success_url = reverse_lazy("books:locations")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование шкафа"
        return context


class ShelfCreateView(CreateView):
    model = Shelf
    form_class = ShelfForm
    template_name = "books/location_form.html"
    success_url = reverse_lazy("books:locations")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["room_id"] = self.request.GET.get("room")
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        cabinet_id = self.request.GET.get("cabinet")
        if cabinet_id:
            initial["cabinet"] = cabinet_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая полка"
        return context


class ShelfUpdateView(UpdateView):
    model = Shelf
    form_class = ShelfForm
    template_name = "books/location_form.html"
    success_url = reverse_lazy("books:locations")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs["room_id"] = self.object.cabinet.room_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование полки"
        return context


class CabinetOptionsView(View):
    def get(self, request):
        room_id = request.GET.get("room_id")
        if not room_id:
            return JsonResponse({"results": []})
        cabinets = Cabinet.objects.filter(room_id=room_id).order_by("name")
        return JsonResponse({"results": [{"id": c.id, "name": c.name} for c in cabinets]})


class ShelfOptionsView(View):
    def get(self, request):
        cabinet_id = request.GET.get("cabinet_id")
        if not cabinet_id:
            return JsonResponse({"results": []})
        shelves = Shelf.objects.filter(cabinet_id=cabinet_id).order_by("name")
        return JsonResponse({"results": [{"id": s.id, "name": s.name} for s in shelves]})
