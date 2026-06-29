from django import template

from books.utils import format_books_on_shelves

register = template.Library()


@register.simple_tag
def books_on_shelves(book_count, shelf_count):
    return format_books_on_shelves(book_count, shelf_count)
