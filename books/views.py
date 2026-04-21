from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import BookFilterForm, BookForm
from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
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
                    | Q(room__icontains=q)
                    | Q(cabinet__icontains=q)
                    | Q(shelf__icontains=q)
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
                qs = qs.filter(room__icontains=room)
            if cabinet:
                qs = qs.filter(cabinet__icontains=cabinet)
            if shelf:
                qs = qs.filter(shelf__icontains=shelf)

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

